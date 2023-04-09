from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

@login_required
def home(request):
    
    if request.method == 'POST':
        subject = f'[Message sent by {request.user.username}@MyApp] {request.POST.get("subject", None)}'
        recipient_list = request.POST.get('recepients', None).split(',')
        body = request.POST.get('body', None)

        try:
            send_mail(subject=subject, recipient_list=recipient_list, message=body, from_email=request.user.email)
        except Exception as e:
            return render(request, 'home.html', { 'error': f'{str(e)}' })
        
        return render(request, 'home.html', { 'success': 'Email sent successfully...' })
        

    return render(request, 'home.html')

def signup(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        try:
            pass
            user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
            user.save()

        except Exception as e:
            return render(request, 'signup.html', {'error': e})
        
        send_signup_email(username, email)

        return render(request, 'signin.html', {'success': f'User with email {email} has been registered successfully, Please login to continue'})

    return render(request, 'signup.html')

def signin(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            send_signin_email(username, user.email)
            return redirect('/')
        else:
            return render(request, 'signin.html', {'error': f'Invalid username or password'})
    else:
        pass


    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('/')

def send_signup_email(username, email):
    subject = 'Welcome to My App!'
    html_content = render_to_string('signup_email.html', {'username': username, 'email': email})
    text_content = strip_tags(html_content)
    
    # create the email, and attach the HTML version as well.
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        to=[email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_signin_email(username, email):
    subject = f'Signin Confirmation [{username}]'
    html_content = render_to_string('signin_email.html')
    text_content = strip_tags(html_content)
    
    # create the email, and attach the HTML version as well.
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        to=[email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()