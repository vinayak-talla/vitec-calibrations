from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, "Username and/or password is invalid. Try again.")

    return render(request, 'login.html', {'timestamp': now().timestamp()})

def logout_user(request):
    logout(request)  # This logs the user out
    messages.success(request, "You have successfully logged out.")
    return redirect('login') 