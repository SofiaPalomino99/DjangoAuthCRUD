from calendar import c
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model): 
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank = True)
    important = models.BooleanField(default=False)
    #foreinkey, relacion de tablas, relacionamos la tabla sql 
    #con la tabla User que se creó para el registro del usuario, el 
    #cascade es para que se eliminen los task si el usuario se elimina
    user =  models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self): 
        #Para que se vea el titulo de la tarea y no Task object() 
        # Para mostrar el usuario que lo hizo, se accede a 
        # el usuario a su nombre de usuario
        return self.title + ' -by ' + self.user.username
