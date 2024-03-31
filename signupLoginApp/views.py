import pickle
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from .models import *
from .filters import *
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required

import  json
import datetime
from datetime import timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']




# Create your views here.
def index_page(request):
    return render(request, 'index.html')



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
            profile_picture = form_obj.cleaned_data['profile_picture']
            
            User.objects.create_user(username=username, password=password,first_name=first_name,last_name=last_name)
            
            profile = UserProfile.objects.create(username=username, password=password, profile_picture=profile_picture, 
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
                current_user = UserProfile.objects.get(username=request.user)
                
                if current_user.designation == 'patient':
                    return redirect('patient_dashboard')
                else:
                    return redirect('doctor_dashboard')
            else:
                return HttpResponse("User does not exist.")           
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
    


@login_required(login_url='/login')
def doctor_dashboard(request):
    current_user=UserProfile.objects.get(username=request.user)
    return render(request, 'doctor_dashboard.html', {"current_user":current_user})



@login_required(login_url='/login')
def patient_dashboard(request):
    current_user=UserProfile.objects.get(username=request.user)
    return render(request, 'patient_dashboard.html', {"current_user":current_user})




def logoutPage(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def createPost_Page(request):
    if request.method == "POST":
        if request.POST.get('draft_id'):
            draft = Draft.objects.filter(pk=int(request.POST.get('draft_id'))).delete()
        title = request.POST.get('postTitle')
        image = request.FILES.get('imageUpload')
        category = request.POST.get('category')
        summary = request.POST.get('summary')
        content = request.POST.get('content')

        post = BlogPost(title=title, image=image, category_id=category, summary=summary, content=content, user=request.user)
        post.save()
        return redirect('blogList')
    
    if request.user.is_authenticated and UserProfile.objects.filter(username=request.user).first().designation == 'doctor':
        categories = Category.objects.all()
        return render(request, 'postBlog.html', {'categories': categories})
    else:
        return redirect('blogList')
        
        

@login_required(login_url='/login')
def createCategory_Page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        
        cat = Category(name=name)
        cat.save()
        return redirect('blogList')
    
    if request.user.is_authenticated and UserProfile.objects.filter(username=request.user).first().designation == 'doctor':
        return render(request, 'addCategory.html')
    else:
        return redirect('blogList')


@login_required(login_url='/login')
def blogList_Page(request):
    if request.method == 'GET' and len(request.GET)>0 and request.GET.get('category') != '':
        posts = BlogPost.objects.filter(category_id = request.GET.get('category'))
    else:
        posts= BlogPost.objects.all()
    categories = Category.objects.all()
    return render(request, 'blogList.html', {'posts':posts, 'categories':categories})


@login_required(login_url='/login')
def blogDetail_Page(request, id):
    blogDetail = BlogPost.objects.get(pk=id)
    return render(request, 'blogDetail.html', {'blogDetail':blogDetail})

@login_required(login_url='/login')
def storeDraft(request):
    if request.method == 'POST':
        title = request.POST.get('postTitle')
        image = request.FILES.get('imageUpload')
        category_id = request.POST.get('category')
        summary = request.POST.get('summary')
        content = request.POST.get('content')

        if request.POST.get('draft_id'):
            # Update existing draft
            draft_id = int(request.POST.get('draft_id'))
            draft = Draft.objects.get(pk=draft_id)
            draft.title = title
            draft.image = image
            draft.category_id = category_id
            draft.summary = summary
            draft.content = content
            draft.user = request.user
            draft.save()
        else:
            # Create new draft
            draft = Draft.objects.create(
                title=title,
                image=image,
                category_id=category_id,
                summary=summary,
                content=content,
                user = request.user
            )

        return JsonResponse({'draftId': draft.id}, safe=False) 
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required(login_url='/login')
def editDraft(request, id):
    if request.user.is_authenticated and UserProfile.objects.filter(username=request.user).first().designation == 'doctor':
        categories = Category.objects.all()
        draft = Draft.objects.filter(pk=id).first()
        return render(request, 'createDraft.html', {'categories': categories, 'draft':draft})
    else:
        return redirect('blogList')
    

@login_required(login_url='/login')
def draftList(request):
    if request.method == 'GET' and len(request.GET)>0 and request.GET.get('category') != '':
        posts = Draft.objects.filter(category_id = request.GET.get('category'))
    else:
        posts= Draft.objects.all()
    categories = Category.objects.all()
    return render(request, 'draftList.html', {'posts':posts, 'categories':categories})

@login_required(login_url='/login')
def doctorList_Page(request):
    doctors = UserProfile.objects.filter(designation = 'Doctor')
    return render(request, 'doctorList.html', { "doctors": doctors })

@login_required(login_url='/login')
def appointment_Page(request, id):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=request.user)
            patient = UserProfile.objects.get(username=user)
            doctor = UserProfile.objects.get(id=id)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return redirect('login')

        if request.method == 'POST':
            speciality = request.POST.get('speciality')
            date = request.POST.get('date')
            start_time = request.POST.get('start-time')

            start_time_dt = datetime.datetime.strptime(start_time, '%H:%M')
            end_time_dt = start_time_dt + datetime.timedelta(minutes=45)
            end_time = end_time_dt.time().strftime('%H:%M')

            appointment = Appointment.objects.create(speciality=speciality, appointment_date=date, start_time=start_time, end_time=end_time)

            with open('token.json', 'r') as f:
                creds = json.load(f)
            credentials = Credentials.from_authorized_user_file('token.json')
            service = build('calendar', 'v3', credentials=credentials)


            datem = datetime.datetime.strptime(date, "%Y-%m-%d")
            stime = datetime.datetime.strptime(start_time, "%H:%M")
            etime = datetime.datetime.strptime(end_time, "%H:%M")

            start_time = datetime.datetime(datem.year, datem.month, datem.day, stime.hour, stime.minute, 0)
            end_time = datetime.datetime(datem.year, datem.month, datem.day, etime.hour, etime.minute, 0)

            event = {
                'summary': 'Patient Appointment',
                'location': 'Mumbai',
                'description': f'Patient Name: {patient.first_name} {patient.last_name}',
                'start': {
                    'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'timeZone': 'Asia/Kolkata',
                },
                'attendees': [{'email': doctor.email_id}],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            event = service.events().insert(calendarId='rkumar90509@gmail.com', body=event).execute()
            context = {'patient': patient, 'appointment': appointment}
            return render(request, 'appointmentConfirmation.html', context)

        return render(request, 'appointmentForm.html')
    else:
        return redirect('login')






@login_required(login_url='/login')
def appointmntList_Page(request):
    return render(request,'appointments.html')


