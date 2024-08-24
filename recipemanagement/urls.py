"""
URL configuration for recipemanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from vege.views import *

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',login_page,name="home"),
    path('receipe/',receipe,name="receipe"),
    path('admin/', admin.site.urls),
    path('update_receipe/<id>/',update_receipe,name="update_receipe"),
    path('delete_receipe/<id>/',delete_receipe,name="delete_receipe"),
    path('login/',login_page,name="login_page"),
    path('register/',register,name="register"),
    path("logout/",logout_page,name="logout_page"),
    path('password_reset/',password_reset, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_done/',password_reset_done, name='password_reset_done'),
    path('password_reset_complete/',password_reset_complete, name='password_reset_complete'),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns+=staticfiles_urlpatterns()