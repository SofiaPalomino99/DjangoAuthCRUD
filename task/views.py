from curses.ascii import HT
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Para hacer el login y hacer la autenticacion
# Para poder registrar a los usuarios con el modelo de Usuario de Django
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate #para crear la cookie, el authenticate es para autenticar 
from django.db import IntegrityError #Para el except 
from .forms import CreateTask
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    home = "Home"
    return render(request, 'home.html', {
        # se crea un diccionario para pasarle informacion al html
        'home': home
    })

def signup(request):
    # print(request.POST) #Para imprimir los datos que se obtuvieron del formulario

    # Verificar si el metodo para obtener la informacion del formulario es POST
    if request.method == 'GET': 
        return render (request, 'signup.html',{'form':UserCreationForm})

    else:
        # si las contraseñas coinciden
        if request.POST['password1'] == request.POST['password2']:
            # try por si falla
            try:
                # Registrar y crear el objeto usuario, usando User.create_user se crea el username
                # igual a request.POST y el username del formulario
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                #Para guardar el usuario
                user.save()
                #Para que entre el usuario y quede guardada la sesion, es el login  
                login(request, user)
                #Si el usuario se guarda se redirecciona a la vista html task
                return redirect('task')
            except IntegrityError:
                #Si falla devuelve el formulario
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "El usuario ya existe"
                })
        #Si las contraseñas no coinciden devuelve el formulario
        return render(request, 'signup.html', {
            # se crea un diccionario para pasarle informacion al html
            'form': UserCreationForm,
            'error' : "Las contraseñas no coinciden"
        }) 

@login_required
def task(request): 
    #Obtener todas las tareas que sean unicamente sel usuario del login
    # (filter), que no estén completadas y guardarlo en la variable tareas
    tareas = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    #Se le envían las tareas a la template task
    return render (request, 'task.html', {
        'tareas':tareas
    })

@login_required
def create_task(request): 
    if request.method == 'GET':
        return render (request, 'create_task.html',{
            #El formulario que se le pasará será el de forms
            'form':CreateTask
        })
    else: 
        try:
            #Crea un formulario a partir de los datos que se envían 
            form = CreateTask(request.POST)
            #Guardar en una variable el formulario nuevo
            new_task = form.save(commit = False)
            #Asignar un usuario porque lo que se guardó fue el 
            #titulo, descripción y important y falta el usuario, 
            # el usuario es el que queda guardado en el login
            new_task.user = request.user
            #Guardar con todos los campos llenos
            new_task.save()     
            return redirect('task')
        except ValueError: 
            return render (request, 'create_task.html',{
            #El formulario que se le pasará será el de forms
            'form':CreateTask, 
            'error' : "Por favor pruebe datos validos"
        })

@login_required
def signout(request): 
    #salir de la sesion 
    logout(request)
    #redirecciona a home
    return redirect('home')

def signin (request): 
    if request.method == 'GET': 
        return render (request, 'signin.html',{
            'form':AuthenticationForm
        })
    else: 
        #autenticar si la request.POST es igual el usuario y la contraseña
        user = authenticate(request, username=request.POST['username'],
                    password=request.POST['password'])
        #Para ver si el usuario está vacío, si no colocó bien los datos
        if user is None: 
            return render (request, 'signin.html',{
                'form':AuthenticationForm, 
                'error': "El usuario o contraseña es incorrecta"
            })
        else:
            #si entra bien, se guarda la sesion con el login
            login(request, user) 
            return redirect('task')

@login_required
def task_detail(request, task_id): #se le envía un id del task 
    #para que muestre unicamente la tarea que se pide (id)
    if request.method == "GET": 
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        #Para llenar el formulario "CreateTask" con los datos de esa tarea, 
        # esto para que se muestre el formulario ya con los campos rellenados
        form = CreateTask(instance=task)
        #se envia al html la tarea del id que se pasó y también el formulario para poder mostrarlos
        return render (request, 'task_detail.html',{'task':task, 'form': form })
    else: 
        try:
            #En task se le pasa la primary key con el id del task obtenido 
            # y también se asegura que solo sean las del usuario 
            task=get_object_or_404(Task,pk=task_id, user= request.user)
            #Se llena el formulario con los datos obtenidos (request.POST), 
            # también se obtienen los datos de la tarea
            form = CreateTask(request.POST, instance=task)
            #Se guardan los cambiso 
            form.save()
            return redirect ('task')
        except ValueError: 
             return render (request, 'task_detail.html',{'task':task, 
                'form': form, 
                'error': "Error al actualizar los datos" 
                })

@login_required
def complete_task(request, task_id): 
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        #si la propiedad de la tarea (datecompleted) ya está como completada 
        task.datecompleted = timezone.now()
        #Se guarda la tarea
        task.save()
        return redirect('task')

@login_required
def delete_task(request, task_id): 
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')

@login_required
def task_completed(request): 
    #Obtener todas las tareas que sean unicamente sel usuario del login
    # (filter), que no estén completadas y guardarlo en la variable tareas
    tareas = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    #Se le envían las tareas a la template task
    return render (request, 'task_completed.html', {
        'tareas':tareas
    })
