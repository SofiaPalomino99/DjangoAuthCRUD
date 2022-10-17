from django import forms
from .models import Task

#Para crear el formulario
class CreateTask(forms.ModelForm): 
    class Meta: 
        #se toma el modelo 
        model = Task 
        #se seleccionan los campos 
        fields = ['title', 'description', 'important']
        widgets = {
            #para cambiar la vista del campo de titulo
            'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Titulo de la nota'}),
            'description': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Descripción de la nota'}),
            'important': forms.CheckboxInput(attrs = {'class': 'form-check-input'})
        }