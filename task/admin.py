from django.contrib import admin
from .models import Task

#para que se muestre la hora de creacion de hace esta clase
class TaskAdmin (admin.ModelAdmin): 
    #Campos de solo lectura de le pasa la tupla de created (hora de creacion )
    readonly_fields= ("created",)

# Register your models here.
#Se le pasa el modelo task y la clase
#para visualizar en el administrador otras cosas
admin.site.register(Task, TaskAdmin)
