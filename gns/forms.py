from django import forms

class queryForm(forms.Form): 
    query = forms.CharField(max_length=1000)

