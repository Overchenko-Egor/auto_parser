from urllib import request
from django.shortcuts import render
from django.http import HttpRequest
from .forms import InputForm






def process_data(input_data):
    # Здесь будет обработка данных, например, создание таблицы
    # Ниже пример создания простой таблицы из строки
    rows = input_data.split()
    table_data = [{'row': row, 'length': len(row)} for row in rows]
    return table_data

def index_page(req):
    if req.method == 'POST':
        form = InputForm(req.POST)
        if form.is_valid():
            input_data = form.cleaned_data['input_text']
            result_table = process_data(input_data)
            return render(req, 'index.html', {'form': form, 'result_table': result_table})
    else:
        form = InputForm()
    
    return render(req, 'index.html', {'form': form})

