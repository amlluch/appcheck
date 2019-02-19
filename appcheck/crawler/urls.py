from django.conf.urls import url
from django.urls import path

from . import views

url_list =[ #It maps url's to the same function
    {'url':"vulnerabilities/captcha/", 'parameter':"Insecure CAPTCHA"},
    {'url':"vulnerabilities/sqli_blind/", 'parameter':"SQL Injection (Blind)"},
    {'url':"instructions.php/", 'parameter':"Instructions"},
    {'url':"setup.php/", 'parameter':"Setup / Reset DB"},
    {'url':"vulnerabilities/brute/", 'parameter':"Brute Force"},
    {'url':"vulnerabilities/exec/", 'parameter':"Command Injection"},
    {'url':"vulnerabilities/csrf/", 'parameter':"CSRF"},
    {'url':"vulnerabilities/fi/", 'parameter':"File Inclusion"},
    {'url':"vulnerabilities/upload/", 'parameter':"File Upload"},
    {'url':"logout.php/", 'parameter':"Logout"},
    {'url':"vulnerabilities/weak_id/", 'parameter':"Weak Session IDs"},
    {'url':"vulnerabilities/xss_d/", 'parameter':"XSS (DOM)"},
    {'url':"vulnerabilities/xss_r/", 'parameter':"XSS (Reflected)"},
    {'url':"vulnerabilities/xss_s/", 'parameter':"XSS (Stored)"},
    {'url':"vulnerabilities/csp/", 'parameter':"CSP Bypass"},
    {'url':"vulnerabilities/javascript/", 'parameter':"JavaScript"},
    {'url':"security.php/", 'parameter':"DVWA Security"},
    {'url':"security.php/phpinfo.php/", 'parameter':"PHP Info"},
    {'url':"about.php/", 'parameter':"About"},
]

generated_list = [path(mi["url"] , views.sqli, {'link':mi["parameter"]}) for mi in url_list]

urlpatterns = [
    path('', views.home, name='home',),
    path('login.php/', views.home, name='home',),
    url(r'^vulnerabilities/sqli/', views.sqli, {'link':'SQL Injection'}),
    
] +  generated_list