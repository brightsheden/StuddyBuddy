from django.core.checks import messages
from django.http import request
from django.shortcuts import render,redirect
#from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import *
from .forms import RoomForm, userForm,MyUserCreationForm
from django.db.models import Q, base
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

#rooms = [
  #  {'id': 1, "name": "let code python"},
   # {'id': 2, "name": "let code javascript"},
    #{'id': 3, "name": "let code java"},
#]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated :
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User doese not exist')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'email or password doese not exist')
        
    context = {"page":page}
    return render (request, 'base/login_registration.html', context)
    
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    #page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, "An error occured durring registration")
 

    context = {"form":form}
    return render(request, "base/login_registration.html", context)
    
            
       
def home(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) |
        Q(description__icontains=q) | Q(host__username__icontains=q))
    
    topic = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = { 'rooms': rooms,
                'topics': topic,
                'room_count': room_count,
                "room_messages":room_messages}

    return render(request, 'base/home.html', context)

def room(request, pk):
    
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all().order_by('-created')
    participants = room.participant.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participant.add(request.user)
        return redirect("room", pk=room.id)


    context = {'room': room,
    "room_message":room_message,
    "participants":participants}

    return render(request, 'base/room.html', context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user,
    "rooms":rooms,
    "room_messages": room_message,
    "topics":topics}
    return render(request, "base/profile.html", context)

@login_required(login_url='login')
def create_room (request):
    form = RoomForm()
    topics =Topic.objects.all()
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name =  request.POST.get('name'),
            description = request.POST.get('description')
        )
        #form = RoomForm(request.POST)
        #if form.is_valid():
            #room = form.save(commit=False)
            #room.host = request.user
            #room.save()

        return redirect("home")
            

    context = {"form":form,
                "topics": topics}

    return render(request , 'base/room_form.html' , context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics =Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name =request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        #form = RoomForm(request.POST, instance=room)
        #if form.is_valid():
            #form.save()
        return redirect("home")

    context = {"form":form, "topics":topics, "room":room}

    return render(request , 'base/room_form.html' , context)

@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect("home")

    return render(request , 'base/delete.html' , {"obj":room})


@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect("home")

    return render(request , 'base/delete.html' , {"obj":message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = userForm(instance=user)
    if request.method == 'POST':
        form = userForm(request.POST,request.FILES ,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    context = {"form":form}
    return render(request, 'base/update-user.html', context)


def Topics(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ""
    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics": topics}
    return render (request, 'base/topics.html', context)


def activityPage(request):
    room_message = Message.objects.all()
    context = {'room_messages':room_message}
    return render (request, 'base/activity.html', context)