from django import forms

class InputForm(forms.Form):
    input_text = forms.CharField(label='Введите текст', max_length=100)
