from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from .models import UserProfile



# Create your views here.
def home_page(request):
    return render(request, 'home.html')



def signup(request):
    if request.method == 'POST':
        form_obj = SignUpForm(request.POST, request.FILES)
        if form_obj.is_valid():
            username = form_obj.cleaned_data['username']
            password = form_obj.cleaned_data['password']
            first_name = form_obj.cleaned_data['first_name']
            last_name = form_obj.cleaned_data['last_name']
            designation = form_obj.cleaned_data['designation']
            email = form_obj.cleaned_data['email']
            password = form_obj.cleaned_data['password']
            address_line1 = form_obj.cleaned_data['address_line1']
            city = form_obj.cleaned_data['city']
            state = form_obj.cleaned_data['state']
            pincode = form_obj.cleaned_data['pincode']
            
            User.objects.create_user(username=username, password=password,first_name=first_name,last_name=last_name)
            
            profile = UserProfile.objects.create(username=username, password=password,
                                                 first_name=first_name,email=email,address_line1=address_line1,
                                                 last_name=last_name,designation=designation,city=city,state=state,pincode=pincode)
            
            
            
            return redirect('login')
    else:
        form_obj = SignUpForm()
    return render(request, 'signup.html', {'form': form_obj})





def user_login(request):
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                current_user=UserProfile.objects.get(username=request.user)
                
                if current_user.designation=='patient':
                      return render(request,'patient_dashboard.html',{'current_user':current_user})
                else:
                    return render(request,'doctor_dashboard.html',{'current_user':current_user})           
    else:
        form = LoginForm()
    return render(request, 'login.html',{'form':form})



def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')


def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

        
def logoutPage(request):
    logout(request)
    return redirect('/')
