from urllib import request
from django.shortcuts import render
from django.http import HttpRequest


def index_page (req):
    return render(req, 'index.html')

