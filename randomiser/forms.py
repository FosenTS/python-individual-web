from django import forms

class InputForm(forms.Form):
    user_input = forms.CharField(label='Ваш ввод', max_length=100)