from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for

from flask_login import login_user, logout_user, login_required, current_user #sesiones
from . import login_manager

from .forms import *
from .models import *
from .consts import *

from .email import * #mail_Server

page = Blueprint('page', __name__)

#funcion a ejecutar cuando: error 400 ocurre
@page.app_errorhandler(404)#decorado (error a trabajar)
def page_not_found(error):#obligatorio parametro "error"
    return render_template('errors/404.html'), 404 #funciones asociadas a un valor DEBEN retornar dos valores, donde, el segundo valor DEBE de ser el error ocurrido

@page.route('/')
def index():
    return render_template('index.html', title = 'Index')#tittle>> nombre que se visualiza en la pestaña del navegador

@login_manager.user_loader
def load_user(id):#retorna un objeto de tipo mixin
    return User.get_by_id(id)

@page.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()#cerrar sesion activa
    flash(LOGOUT)
    return redirect(url_for('.login'))

#pintar formulario login
@page.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated: #valida si el usuario a inicado sesion y lo re dirige a otro lguar
        return redirect(url_for('.tasks'))

    form = LoginForm(request.form)#request.form permite obtener los valores de los campos del formulario (nombre_form.nombre_formulario.data)

    if request.method == 'POST':
        if form.validate():
            user = User.get_by_username(form.username.data)
            if user and user.verify_password(form.password.data): 
                login_user(user)#espera un objeto user.mixin / inicio de sesion???
                flash(LOGIN)
                return redirect(url_for('.tasks'))
            else:
                flash(ERROR_FORMULARIO_LOGIN , 'error')#segundo argumento indica la categoria            
        else:
            print('Campos no validados')
    return render_template('auth/login.html', title = 'Login', form = form)

@page.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:#valida si el usuario a inicado sesion y lo re dirige a otro lguar
        return redirect(url_for('.tasks'))

    form = RegisterForm(request.form)#request.form permite obtener los valores de los campos del formulario (nombre_form.nombre_formulario.data)

    if request.method == 'POST':
        if form.validate():
            user = User.create_element(form.username.data, form.password.data, form.email.data)
            flash(USER_CREATED)
            print("usuario creado")
            print(user.id)
            login_user(user)#espera un objeto user.mixin / inicio de sesion???
            welcome_mail(user, "user") # mail_server
            return redirect(url_for('.tasks'))
        else:
            print('Campos no validados')
    return render_template('auth/register.html', title = 'register', form = form)

@page.route('/tasks', methods = ['GET', 'POST'])#solo podra acceder un usuario con una sesion activa (inicio session)
@page.route('/tasks/<int:page>', methods = ['GET', 'POST']) #pagination
@login_required #solo podra ingresar el usuario autenticado(inicio session)
def tasks(page = 1, per_page = 2): #lista_tareas / priemr parametro permite saber en que pagina se esta / segundo parametro da a conocer los elementos a mostrar por pagina
    #tasks = current_user.tasks_user_id.paginate() # por medio de current user podemos traer toda la informacion de una variable relacionada (llave foranea) en este caso tasks
    pagination = current_user.tasks_user_id.paginate(page, per_page = 2)#paginacion de elementos
    tasks = pagination.items

    return render_template('task/list.html', title = 'Tareas', tasks = tasks, pagination = pagination, page = page)

@page.route('/tasks/new', methods = ['GET', 'POST'])#solo podra acceder un usuario con una sesion activa (inicio session)
@login_required #solo podra ingresar el usuario autenticado(inicio session)
def new_task(): #añadir nueva tarea
    form = TaskForm(request.form)

    if request.method == 'POST':
        if form.validate():
            task = Task.create_element(form.title.data, form.description.data, current_user.id)#current_user.id retorna el ide del usuario actualmente logueado
            if task:
                flash(TASK_CREATE)

            return redirect(url_for('.tasks'))
        else:
            print('Campos no validados')

    return render_template('task/new.html', title = 'Nueva tarea', form = form)

@page.route('/tasks/show/<int:task_id>', methods = ['GET', 'POST'])#solo podra acceder un usuario con una sesion activa (inicio session)
@login_required #solo podra ingresar el usuario autenticado(inicio session)
def get_task(task_id): #visualizar la tarea de la lista en otra pagina
    task = Task.query.get_or_404(task_id)

    return render_template('task/show.html', title = 'Tarea', task = task)

@page.route('/tasks/delete/<int:task_id>', methods = ['GET', 'POST'])#solo podra acceder un usuario con una sesion activa (inicio session)
@login_required #solo podra ingresar el usuario autenticado(inicio session)
def delete_task(task_id): #borrar elemento de la db
    task = Task.query.get_or_404(task_id)

    if task.tasks_user_id != current_user.id:
        abort(404)

    if Task.delet_element(task.id):
        flash('tarea eliminada')
    
    return redirect(url_for('.tasks'))

