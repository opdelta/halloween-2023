from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from wordgame.models import Wordgame
# Import ButtonPressed model
from wordgame.models import ButtonPressed
import random
import time
import json
# Create your views here.

def home_view(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def wheel_view(request):
    return render(request, 'wheel.html')

def test_view(request):
    return render(request, 'test.html')
# def home_view(request, context={}):
# 
#     if not request.user.is_authenticated or request.user.is_anonymous:
#         return redirect('login')
#     
#     if request.method == 'POST':
#         set_word_variable(request)
#         user = request.user
#         userid = user.id
#         csrf = request.COOKIES['csrftoken']
#         print("user is " + user.username)
#         print("userid is " + str(userid))
#         print("csrf is " + csrf)
#         item = ButtonPressed.objects.create(user=str(user), csrf=csrf)
#         item.save()
#         return redirect('home')
#     
#     return render(request, "home.html", context)
# 
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'You are now logged in')
#             request = set_word_variable(request)
#             return redirect('home')
#         else:
#             messages.error(request, 'Mauvais identifiants!')
#             return redirect('login')
#     if request.user.is_authenticated and not request.user.is_anonymous:
#         return redirect('home')
#     
#     return render(request, 'login.html', {})
# 
# def set_word_variable(request):
#     num = random.randint(17, Wordgame.objects.count())
#     try:
#         obj = Wordgame.objects.get(id=num)
#         print(obj)
#         word = obj.word
#     except Wordgame.DoesNotExist:
#         word = "Oops! Vous aviez 1 chance sur " + str(Wordgame.objects.count()) + " de tomber sur ce mot. Vous devez appuyer sur le bouton, sinon une conséquence vous sera attribuée."
# 
#     request.session['word'] = word
#     return request
# 
# def logout_view(request):
#     logout(request)
#     return redirect('login')
# 
# def words_detail_view(request):
#     if not request.user.is_authenticated or request.user.is_anonymous:
#         return redirect('login')
#     
#     if request.method == 'POST':
#         set_word_variable(request)
#         return redirect('wordgame')
#     
#     return render(request, 'wordgame.html', {})
# 
# def wheel_view(request):
#     if not request.user.is_authenticated or request.user.is_anonymous:
#         return redirect('login')
#     print(request.META)
#     return render(request, 'wheel.html', {})
# 
# def channel_message(self, event):
#     message = event['message']
#     self.send(text_data=json.dumps({
#         'message': message
#     }))
# 
# def send_wheel_spin(userid, csrf):
#     url = "http://localhost:8000/wheel/spin"
#     data = {
#         'userid': userid,
#         'csrfmiddlewaretoken': csrf
#     }
#     response = requests.post(url, data=data)
#     print(response.text)
#     return response.text
# 
# def test_view(request):
#     
#     try:
#         count = len(ButtonPressed.objects.all())
#     except ButtonPressed.DoesNotExist:
#         count = 0
#     return HttpResponse(count)