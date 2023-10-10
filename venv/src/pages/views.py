from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import datetime
import re
from django.conf import settings
from countdown.models import Countdown
import os
# Create your views here.

def home_view(request):
    user_info = f"User IP: {request.META['REMOTE_ADDR']} | User Agent: {request.META['HTTP_USER_AGENT']}"
    print(user_info)
    contact_form_path = settings.BASE_DIR / 'static' / 'feedbacks'  # Construct absolute path
    if request.method == 'POST':
        name = request.POST.get('name')
        # remove spaces and special characters from name with regex
        name = re.sub(r'\W+', '', name)

        email = request.POST.get('email')
        message = request.POST.get('message')
        # get current datestamp from system
        datestamp = datetime.datetime.now()
        # Format the datestamp to a valid format for file names
        formatted_datestamp = datestamp.strftime('%Y-%m-%dT%H%M%S')
        print(datestamp)

        # Process the form data here (e.g., save to the database)
        # Redirect back to the same page after processing the form
        print("name is " + name)
        print("email is " + email)
        print("message is " + message)
        # Save the data as a new txt file in relative path ../static/feedbacks/name-datestamp.txt
        file_path = os.path.join(contact_form_path, f"{name}-{formatted_datestamp}.txt")
        with open(file_path, 'w') as f:
            f.write('Name: ' + name + '\n')
            f.write('Email: ' + email + '\n')
            f.write('Message: ' + message + '\n')
            f.write('Datestamp: ' + formatted_datestamp + '\n')
        
        return redirect('home')  # Redirect to the home page after form submission

    return render(request, 'index.html')


def login_view(request):
    return render(request, 'login.html')

def test_view(request):
    return render(request, 'test.html')

def submit_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Do something with the form data, e.g., save it to the database

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Form submitted successfully'})

    return JsonResponse({'message': 'Invalid request method'}, status=400)

def login_view(request):
     if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(request, username=username, password=password)
         if user is not None:
             login(request, user)
             messages.success(request, 'You are now logged in')
             if request.user.username == "CuriedePompée":
                return redirect('timeturner')
             else:
                #Disconnect the user
                logout(request)
         else:
             messages.error(request, 'Mauvais identifiants!')
             return redirect('login')
     if request.user.is_authenticated and not request.user.is_anonymous:
            if request.user.username == "CuriedePompée":
                return redirect('timeturner')
     
     return render(request, 'login.html', {})
 
def timeturner_view(request):
    return render(request, 'timeturner.html')

