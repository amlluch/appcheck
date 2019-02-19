import pickle
from django.http import HttpResponse

from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from .utils import ParseElems, RemoteLogin
from .forms import GenericForm
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.template import Template, Context
from django import forms
from django.views.generic import TemplateView, View
from django.http import HttpResponseRedirect
from selenium.common.exceptions import NoSuchElementException
from .models import TargetSite, LinkedSite


@csrf_exempt
def home(request):
# Open the session
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    browser = webdriver.PhantomJS()
    try:
        target = TargetSite.objects.get(active = True)
    except:
        response = render(request, '404.html',)
        response.status_code = 404
        return response
    url = target.uri
    timeout = target.timeout
    browser.set_page_load_timeout(timeout)
    try:
        browser.get(url)
        elem = browser.find_element_by_xpath("//*")
        
        source_code = elem.get_attribute("outerHTML")
        page_to_render = ParseElems(source_code, )
        page_to_render.clean(url)

    # user and password form
        fields, method, names = page_to_render.addform('{{ dynamicform }}')
        DynamicForm = type ('DynamicForm', (GenericForm,), fields)
    except:
        response = render(request, '404.html',)
        response.status_code = 404
        return response

    t = Template(page_to_render)
    if request.method == method:
        form = DynamicForm(request.POST)

        if form.is_valid():
            # gets user and password and sends with Selenium
            user = form.cleaned_data['field_1']
            password = form.cleaned_data['field_2']

            try:
                login = RemoteLogin(user, password, timeout, url, link = '') # log in now
            except:
                response = render(request, 'nologin.html',)
                response.status_code = 401
                return response
            browser = login.get_browser() 
            elem = browser.find_element_by_xpath("//*")
            source_code = elem.get_attribute("outerHTML")
            page_to_render = ParseElems(source_code, )
            page_to_render.clean(url)

            t = Template(page_to_render)
# Stores user and password for next sessions
            browser_session = {'user':user, 'password':password}
            request.session['browser'] = browser_session

            return HttpResponse(t.render(Context()))
    else:
        form = DynamicForm()
        

    return HttpResponse ( t.render(Context({'dynamicform':form})))

@csrf_exempt
def sqli(request, link = None):
    # if user and password doesn't exist, returns to login page
    if 'browser' not in request.session:
        return HttpResponseRedirect('/')
    elif not request.session['browser']:
        return HttpResponseRedirect('/')

    user = request.session['browser']['user']
    password = request.session['browser']['password']
 #   link = 'SQL Injection'
    target = TargetSite.objects.get(active = True)
    url = target.uri
    timeout = target.timeout
    # logs in
    try:
        login = RemoteLogin(user, password, timeout, url, link = link)
    except:
        response = render(request, 'nologin.html',)
        response.status_code = 401
        return response

    browser = login.get_browser() 
    elem = browser.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    page_to_render = ParseElems(source_code, )
    page_to_render.clean(url)
    # Detects inputs, gets the structure and generates dynamic form
    fields, method, names = page_to_render.addform('{{ dynamicform }}')

    if  method not in ['POST', 'GET']:  # if there is no form, just return the html
        t = Template(page_to_render)
        return HttpResponse(t.render(Context()))
    # Here the dynamic form
    DynamicForm = type ('DynamicForm', (GenericForm,), fields)

    t = Template(page_to_render)
    #ok ... let's read the data in form
    if request.method == method:
        request_method = request.POST if method == 'POST' else request.GET
        form = DynamicForm(request_method)

        if form.is_valid():  # data is ok but ... any bad attemp?

            cont = 0
            # Fills all forms ...
            for field in fields:
                
                # Any attack will be prosecuted!
                attack_control = LinkedSite.objects.filter(linkname = link)
                if attack_control:
                    escapes = ''.join([chr(char) for char in range(1, 32)]) + '"%\_' + "'"   
                    original_value = form.cleaned_data['field_' + str(cont+1)]
                    if (any(elem in original_value for elem in escapes)):
                        response = render(request, 'injection.html',)
                        response.status_code = 401
                        return response
                elem = browser.find_element_by_name(names[cont])
                elem.send_keys(form.cleaned_data['field_' + str(cont+1)])
                cont += 1
            # ... and we send the data
            elem.send_keys(Keys.RETURN)
            elem = browser.find_element_by_xpath("//*")
            source_code = elem.get_attribute("outerHTML")
            page_to_render = ParseElems(source_code, )
            page_to_render.clean(url)
            # Insert again the form for next round
            fields, method, names = page_to_render.addform('{{ dynamicform }}')
            DynamicForm = type ('DynamicForm', (GenericForm,), fields)
            t = Template(page_to_render)
            return HttpResponse(t.render(Context({'dynamicform':form})))
        else:
            form = DynamicForm()
    try:   # there are hidden forms
        return HttpResponse(t.render(Context({'dynamicform':form})))
    except:
        return HttpResponse(t.render(Context()))
