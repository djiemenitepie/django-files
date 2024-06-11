from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo3
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo3 = Todo3(user=request.user, name=task)
        new_todo3.save()

    all_todo3s = Todo3.objects.filter(user=request.user)
    context = {
        'todo3s': all_todo3s
    }
    return render(request, 'todoapp3/todo3.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Error, username already exists. Use another.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'todoapp3/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')

    return render(request, 'todoapp3/login.html', {})

# @login_required
# def DeleteTask(request, todo3_name):
#     get_todo3 = get_object_or_404(todo3, user=request.user, todo3_name=todo3_name)
#     get_todo3.delete()
#     return redirect('homepage')

# @login_required
# def Update(request, name):
#     get_todo3 = get_object_or_404(todo3, user=request.user, todo3_name=name)
#     get_todo3.status = True
#     get_todo3.save()
#     return redirect('homepage')

@login_required
def delete_todo3(request, todo3_id):
    todo = Todo3.objects.get(id=todo3_id, user=request.user)
    todo.delete()
    return redirect('home')

# @login_required
# def update_todo3(request, todo3_id, status):
#     todo = Todo3.objects.get(id=todo3_id, user=request.user)
#     todo.status = status
#     todo.save()
#     return redirect('home')


@login_required
def update_todo3(request, todo3_id, status):
    todo = Todo3.objects.get(id=todo3_id, user=request.user)
    todo.status = (status.lower() == 'true')
    todo.save()
    return redirect('home')  # Ensure this name matches the URL pattern name in urls.py