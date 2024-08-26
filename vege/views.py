from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q,Sum #for or condition

from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm


@login_required(login_url="/login/")
def receipe(request):
    if request.method == "POST":
        data=request.POST
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        receipe_image=request.FILES.get('receipe_image')
        
        Receipe.objects.create(receipe_name=receipe_name,
                               receipe_description=receipe_description,
                               receipe_image=receipe_image)
        return redirect('/receipe/')
    queryset=Receipe.objects.all()
    
    if request.GET.get('search'):
        queryset=queryset.filter(receipe_name__icontains = request.GET.get('search'))
    
    context={'receipes':queryset}
    return render(request,'receipe.html',context)

@login_required(login_url="/login/")
def delete_receipe(request,id):
    queryset=Receipe.objects.get(id=id)
    queryset.delete()
    # return HttpResponse("a")
    return redirect('/receipe/')

@login_required(login_url="/login/")
def update_receipe(request,id):
    queryset=Receipe.objects.get(id=id)
    
    if request.method == "POST":
        data=request.POST
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        receipe_image=request.FILES.get('receipe_image')
        
        queryset.receipe_name=receipe_name
        queryset.receipe_description=receipe_description
        
        if receipe_image:
            queryset.receipe_image=receipe_image
            
        queryset.save()
        return redirect('/receipe/')
        
    context={'receipes':queryset}

    # return HttpResponse("a")
    
    return render(request,'update_receipe.html',context)

@login_required(login_url="/login/")
def see_receipe(request,id):
    queryset=get_object_or_404(Receipe, id=id)
    context={'receipes':queryset}
    return render(request,'seerecipe.html',context)

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password=request.POST.get('password')
        
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email does not exist")
            return redirect('/login/')
        
        user=authenticate(username=email,password=password)
        
        if user is None:
            messages.error(request, "Invalid password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/receipe/')
            
            
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect("/login/")
    

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from django.contrib import messages
from .forms import RegistrationForm
    
# def register(request):
#     if request.method == "POST":
#         first_name=request.POST.get("first_name")
#         last_name=request.POST.get("last_name")
#         email = request.POST.get("email")
#         password=request.POST.get("password")
        
#         if User.objects.filter(email=email).exists():
#             messages.info(request, "Email already taken")
#             return redirect('/register/')
        
#         user=User.objects.create(
#             first_name=first_name,
#             last_name= last_name,
#             username=email,
#             email=email
#         )
        
#         user.set_password(password)
#         user.save()
#         messages.info(request, "Account created successfully")
        
#         return redirect("/register/")
#     return render(request,'register.html')

from .forms import RegistrationForm

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('/login/')
        # else:
        #     # Display form errors
        #     for field, errors in form.errors.items():
        #         for error in errors:
        #             messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def password_reset_complete(request):
    if request.method == "POST":
        return redirect("/login.html")
    
    return render(request, 'password_reset_complete.html')


def password_reset(request):
    if request.method == "POST":
        data=request.POST
        email=data.get('email')
        if not User.objects.filter(username=email).exists():
            messages.error(request, "Username does not exist")
            return redirect('/login/')
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        reset_link = f"http://{current_site.domain}/password_reset_confirm/{uid}/{token}/"
        
        send_mail(
            'Password Reset Request',
            f'Please use the following link to reset your password: {reset_link}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return redirect('/password_reset_done/')
    
    return render(request, 'password_reset_form.html')

def password_reset_confirm(request, uidb64, token):
    if request.method == "POST":
        data = request.POST
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user and default_token_generator.check_token(user, token):
            if new_password1 == new_password2:
                form = SetPasswordForm(user, {'new_password1': new_password1, 'new_password2': new_password2})
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, user)
                    return redirect('/password_reset_complete/')
                else:
                    # for field, errors in form.errors.items():
                    for errors in form.errors.items():
                        for error in errors:
                            # messages.error(request, f"{field}: {error}")
                            messages.error(request, f"{error}")
                    messages.error(request, "Invalid form submission.")
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "Invalid reset link.")
        
    return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')  