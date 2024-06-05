from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        birthdate = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        profile_image = request.FILES.get('profile_image')
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            return render(request, 'login-register.html', {'error': 'Email already registered'})

        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        # Create the user profile
        profile = Profile(
            user=user,
            birthdate=birthdate,
            gender=gender,
            phone_number=phone_number,
            profile_image=profile_image
        )
        profile.save()

        # Log the user in
        user = authenticate(request, username=email, password=password)
        login(request, user)

        return redirect('dashboard')  # Change 'dashboard' to your desired URL name

    return render(request, 'login-register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Log the user in
            login(request, user)
            
            # Redirect to a success page or dashboard
            return redirect('dashboard')  # Change 'dashboard' to your desired URL name
        else:
            # Handle invalid login credentials
            return render(request, 'login-register.html', {'error': 'Invalid email or password'})

    return render(request, 'login-register.html')

@login_required
def dashboard(request):
    # Add any logic here that you want to execute when the user accesses the dashboard
    return render(request, 'home.html')