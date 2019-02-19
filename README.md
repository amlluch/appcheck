<h2>Installation</h2>

This app is developed with django and uses postgresql as database. You can install inside a virtualenv or in a docker. This instructions are for docker.

1) Build the application:  <strong>docker-compose build</strong><br>
2) Start the application for installing postgres: <strong>docker-compose up</strong><br>
3) Migrate data (3 steps):<br>
  3.1 <strong>docker-compose run --rm appcheck /bin/bash -c "cd appcheck; ./manage.py migrate"</strong><br>
  3.2 <strong>docker-compose run --rm appcheck /bin/bash -c "cd appcheck; ./manage.py makemigrations crawler"</strong><br>
  3.3 <strong>docker-compose run --rm appcheck /bin/bash -c "cd appcheck; ./manage.py migrate"</strong><br>
4) Create super-user: <strong>docker-compose run --rm appcheck /bin/bash -c "cd appcheck; ./manage.py createsuperuser"</strong><br>

Now you can start the app with docker: <strong>docker-compose up</strong>

<h2>Configuration</h2>
This application carwls a target site, so it is necessary to indicate the address of the site. You can configure several sites, but only one of them will be active. To do this, log in as super-user at http://your-url/admin . After this, under "CRAWLER" click on 
 "Destination site lists", enter the data of the destination site (url, port, timeout) and set it to "active".<br><br>

The application crawls the entire site. To detect injection code attempts, you must indicate the link to crawl. You can indicate it
clicking on "Link names to control injections" and indicating the text of the link ("SQL Injection" for this exercise, but you can enter any of the active links).<br><br>

You can install a DVWA image or simply run it in a docker: <strong>docker run -d --rm -it -p 80:80 vulnerable/web-dvwa</strong> or enter one that is already running at http://docker.anonvpn.es/ . You can try this application at http://docker.anonvpn.es:8000. This is a Docker application that is running.

<h2>Architecture</h2>

The app is made with django. The app uses Selenium to track the target site. Once downloaded the page uses "BeautifulSoup" as a parser and and adapts all addresses of the style files, images, etc. remotely accessed. The local links are preserved as they are because it will use them to access other parts of the remote server from django.

With BeautifulSoup it reads all the forms and replaces them with  django forms that will use for analyzing if there has been an attempt to inject malicious code. The app uses the django admin site for storing local data in a postgresql database.
