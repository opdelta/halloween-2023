"""halloween URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
import pages.views
import countdown.views
0
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pages.views.home_view, name='home'),
    path('login/', pages.views.login_view, name='login'),
    path('countdown/', countdown.views.countdown_view, name='countdown'),
    path('api/get_target_date/', countdown.views.get_target_date, name='get_remaining_time'),
    re_path(r'^api/add_time/(?P<number>\d+)(?P<time_indicator>[smh])/$', countdown.views.add_time, name='add_time'),
    re_path(r'^api/remove_time/(?P<number>\d+)(?P<time_indicator>[smh])/$', countdown.views.remove_time, name='add_time'),
    path('api/reset_target_date/', countdown.views.reset_target_date, name='reset_target_date'),
]

