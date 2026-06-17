from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.

# Define a view function for the registration page
def register(request):
    if request.method == 'POST':
        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Creates user and securely hashes the password
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}!')
            return redirect('userlogin:login')  # Redirects to your login page
        else:
            messages.info(request, 'Invalid username/password')
            
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


    
def login_user(request):

    if request.method == 'POST':
    
        form = AuthenticationForm(request, data=request.POST)
    
        if form.is_valid():
        
            user = form.get_user()
        # Grab credentials from your custom HTML form or Django form

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
        
        
            user = authenticate(request, username=username, password=password)
         

            if user is not None:
                login(request, user) # Creates a cookie-backed session
                return redirect('index')
            else:
                messages.error('Invalid credentials')
                return render(request, 'login.html')

    else:
            form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    if request.method=='POST':
        logout(request)
        
        messages.info(request,'You have been Logged Out successfully.....')
        return render(request,'logout.html')

    return render(request,'logout.html')
