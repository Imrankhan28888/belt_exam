from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from .models import *
from django.contrib import messages
from django.db.models import Count

def index(request):
    context = {
    "time": strftime("%b %d, %Y  %H:%M %p", gmtime())
    }
    return render(request, "index.html", context)
   

def register(request):
    if request.method == "GET":
        return redirect("/")
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/thoughts')


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/thoughts')

def logout(request):
    request.session.clear()
    return redirect('/')




def thoughts(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'all_thoughts':Thought.objects.annotate(likes=Count("users_likes")).order_by("-likes") 
              
    }
    return render(request, 'thoughts.html', context)

def post_thought(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Thought.objects.validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/thoughts')
        
        if request.method == "POST":
            Thought.objects.create(
                message=request.POST['message'],
                user_uploaded = User.objects.get(id=request.session['user_id'])
            )
    
    return redirect('/thoughts')

def show_thought(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    thought = Thought.objects.get(id=id)
    
    context = {
        'user': user,
        'thought': thought,
    }

    return render(request, 'show.html', context)

def delete_thought(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        delete_thought = Thought.objects.get(id=id)
        print("session user id: " + str(request.session['user_id']))
        print("Message user id: " + str(delete_thought.user_uploaded.id))
        if ((request.session['user_id']) == delete_thought.user_uploaded.id):
            delete_thought.delete()
    
    return redirect('/thoughts')


def favorite(request, thought_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session["user_id"])
        thought = Thought.objects.get(id=thought_id)
        user.users_liked_thoughts.add(thought)
        context = {
            'user': user,
            'thought': thought,
        }

    return render(request, 'show.html', context)



def unfavorite(request, thought_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session["user_id"])
        thought = Thought.objects.get(id=thought_id)
        user.users_liked_thoughts.remove(thought)
        context = {
            'user': user,
            'thought': thought,
        }

    return render(request, 'show.html', context)
