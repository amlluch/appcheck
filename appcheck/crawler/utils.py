from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from django import forms

import os

class ParseElems():

    def __init__(self, htmlview):
        self.htmlview = htmlview

    def _hrefs(self, element, ref, url, sanitize = False):  # we want that points to the target url

        soup = BeautifulSoup(self.htmlview, features="html.parser")

        for link in soup.findAll(element):
            reference = link.get(ref)
            if not reference:   #not found ... sometimes happens
                return
            if ('http' or 'https') not in reference:
                if sanitize:    # a tags just sanitize the address but should point to local
                    new_href = os.path.normpath(reference) + '/'
                else:
                    new_href = url + os.path.normpath(reference) 
                link[ref] = link[ref].replace(reference, new_href)
        self.htmlview = str(soup)

    def addform(self, django_form):     # changes the actual form for a django form one

        soup = BeautifulSoup(self.htmlview, features="html.parser")
        total_forms = soup.findAll('form')
        
        if not total_forms:     #if there is no form, return
            return None, '', None
        # soup.form.insert_after('{% csrf_token %}', django_form)
        for form in total_forms:

            del form['action']  #remove original action
            method = form['method'].upper()
# get data from form and create fields for a form class
            fields_form = {}
            cont_field = 0
            names = []  # here the input names attribute
            myforms = form.findAll('input')

            for input_tag in myforms:
                
                if input_tag['type'] in ['text', 'password', 'textarea']: #only for this type of fields
                    cont_field += 1
                    label = input_tag['name']
                    attrlist = input_tag.attrs  # get all attributes
                    
                    names.append(label)
                    attrlist.pop('name')    # name attribute is in a label, remove it
                    if 'class' in attrlist: # calculate css class
                        convert_class = ''
                        for el_class in attrlist['class']:
                            convert_class = el_class + ' '
                        attrlist['class'] = convert_class
                    # create the field for dynamic form. only parsing charfields
                    myfield = {'field_' + str(cont_field):forms.CharField(label = label.capitalize(), widget = forms.TextInput(attrs=attrlist))}
                    fields_form.update(myfield)
                    # remove old input fields and labels
                    if input_tag.find_previous_sibling('label'):
                        input_tag.find_previous_sibling('label').decompose() #remove label tags if exist
                    input_tag.decompose()

            if not names:   # if not valid inputs, return
                return None, '', None

            myform = form.find('fieldset')

            if myform:  # if there is a fieldset tag inside the form, put after it inside the django form
                myform.insert(0, NavigableString(django_form))
            else:
                form.insert(0, NavigableString(django_form))

        self.htmlview = str(soup)
        return fields_form, method, names

    def clean(self, url): # It cleans all the code and changes url's

        self._hrefs('link', 'href', url)    # get css
        self._hrefs('img', 'src', url)      # img url
        self._hrefs('a', 'href', url, sanitize = True)  # for 'a' tag
        self._hrefs('script', 'src', url)   # get the scripts

    def __str__(self):
        return self.htmlview
    
class RemoteLogin():    # Each time we need log in (django losses selenium session)

    def __init__(self, user, password, timeout, home,  link):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
#        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser = webdriver.PhantomJS()
        self.browser.set_page_load_timeout(timeout)      # set timeout
        self.browser.get(home)
        elem = self.browser.find_element_by_name('username')
        elem.send_keys(user)
        elem = self.browser.find_element_by_name('password')
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)     # sends user and password to target url
        if link:    # clicks on link using selenium
            elem = self.browser.find_element_by_link_text(link)
            elem.click()
    
    def get_browser(self):
        return self.browser

    def __repr__(self):
        return self.browser

        