from django.shortcuts import render, redirect
from .forms import UserRegistrationForm , LoginForm , ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.user_type == 'seller':
                    return redirect('shop:seller_dashboard')
                else:
                    return redirect('shop:product_list')
            else:
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'error': 'Invalid credentials'
                })
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('shop:product_list')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, 
            request.FILES,  # Required for file uploads
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

# views.py
@login_required
def delete_profile_image(request):
    if request.method == 'POST':
        request.user.profile_picture.delete()
        return redirect('profile')
    return redirect('profile')