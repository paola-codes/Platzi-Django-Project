# Platzi: Django Store Project


This a follow-along project from Platzi's Django Intermediate course on Testing, Static Files, and Django Admin at https://platzi.com/cursos/django-intermedio/

## Description

This project is made of python, python templates and a Django database; front-end is limited but present. The api creates questions, and each one can get votes. The point of this project is to practice django.

## Getting Started

* Its best to follow the course tutorial.

### Executing program

* First, open two separate terminals, one for the server and one for the front-end
* For both, make sure your path looks somewhat like this: C:\Users\myname\Desktop\django-platzi\premiosplatzi
* Then, follow these commands in order (for both server and front-end)
```
.\venv\Scripts\activate
cd premiosplatziapp
```
* After, that run this command ONLY on the terminal for the server
```
py manage.py runserver
```
* For the front-end, copy the local address that the terminal gives you and paste on the browser to see your front-end, it may look like this: http://127.0.0.1:8000/
* It will say "Page not found," so add /poll at the end like this http://127.0.0.1:8000/polls/
* That is all.

## Acknowledgments

Original Project:
* https://platzi.com/cursos/django-intermedio/
