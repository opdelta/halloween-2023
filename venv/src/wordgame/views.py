import random
from django.shortcuts import render

# Create your views here.
from .models import Wordgame

def words_detail_view(request):
    # random number between 1 and number of words
    num = random.randint(1, Wordgame.objects.count())
    obj = Wordgame.objects.get(id=num)
    context = {
        'object': obj.word
    }
    return render(request, "wordgame/detail.html", context)