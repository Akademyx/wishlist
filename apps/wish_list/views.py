# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from datetime import date
import bcrypt
from django.db.models import Q
from django.utils.dateparse import parse_date

# Create your views here.
def main(request):
    return render(request, "main.html")

def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    items = Wish_item.objects.filter(Q(others=user)|Q(created_by=user))
    everyone = Wish_item.objects.exclude(Q(others=user) | Q(created_by=user))

    context={
        "me": user,
        "items": items,
        "others": everyone
    }
    return render(request, "dashboard.html", context)

def wish_item(request, id):
    o = Wish_item.objects.get(id=id)
    u = o.others.all()


    context={
        "item":o,
        "others":u
    }
    return render(request, "item_info.html", context)

def create_form(request):
    return render(request, 'create.html')


def register(request):
    errors = []

    if len(request.POST['name']) < 3:
        errors.append("Name field must be at least three characters")
    if len(request.POST['username']) < 3:
        errors.append("Username field must be more than three characters")
    if len(request.POST['pwd']) < 8:
        errors.append("Password length must be at least 8 characters long")
    elif request.POST['pwd'] != request.POST['pwdc']:
        errors.append("Password and password confirmation don't match.")


    if errors:
        for err in errors:
            messages.error(request, err)

        return redirect('/main')

    else:
        try:
            User.objects.get(email=request.POST['email'])
            messages.error(request, "User with that email already exists.")
            return redirect('/main')
        except User.DoesNotExist:

            hashpw = bcrypt.hashpw(
                request.POST['pwd'].encode(), bcrypt.gensalt())
            users = User.objects.create(name=request.POST['name'],
                                        username=request.POST['username'],
                                        password=hashpw,
                                        email=request.POST['email'],
                                        date_hired=request.POST['date_hired'])
            request.session['user_id'] = users.id

            return redirect('/dashboard')


def login(request):
    try:
        user = User.objects.get(email=request.POST['em'])
        # bcrypt.checkpw(given_password, stored_password)
        if bcrypt.checkpw(request.POST['pass'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            messages.error(request, "Email/Password combination FAILED")
            return redirect('/main')
    except User.DoesNotExist:
        messages.error(request, "Email does not exist. Please try again")
        return redirect('/main')


def logout(request):
    request.session.clear()
    return redirect('/main')

def add_item(request):
    i = User.objects.get(id=request.session['user_id'])

    if len(request.POST['i_name']) < 3:
        messages.error(request, "Needs to be at least 3 characters Long")
        return redirect('/wish_items/create')
    else:
        Wish_item.objects.create(item=request.POST['i_name'], created_by=i)
        return redirect('/dashboard')

def delete(request, id):
    i = User.objects.get(id=request.session['user_id'])
    a = Wish_item.objects.get(id=id)
    i.others_created.remove(a)
    return redirect('/dashboard')

def delete_mine(request, id):
    i = User.objects.get(id=request.session['user_id'])
    b = Wish_item.objects.get(id=id)
    b.delete()
    return redirect('/dashboard')

def join(request, id):
    a = Wish_item.objects.get(id=id)
    i = User.objects.get(id=request.session['user_id'])
    a.others.add(i)
    a.save()

    return redirect('/dashboard')