from urllib import request
from django.shortcuts import render
from django.http import HttpRequest
from .forms import InputForm
import requests
from bs4 import BeautifulSoup
import parser.main






def process_data(input_data):
    
    dat = parser.main.p_masuma(input_data)

    # table_data = [{'dat': dat}]
    return dat

def index_page(req):
    if req.method == 'POST':
        form = InputForm(req.POST)
        if form.is_valid():
            input_data = form.cleaned_data['input_text']
            result_table = process_data(input_data)
            print (result_table)
            return render(req, 'index.html', {'form': form, 'result_table': result_table})
    else:
        form = InputForm()
    
    return render(req, 'index.html', {'form': form})

