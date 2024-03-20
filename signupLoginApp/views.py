from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from .models import *
from .filters import *
from django.http import JsonResponse,HttpResponse




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


def blogList_Page(request):
    if request.method == 'GET' and len(request.GET)>0 and request.GET.get('category') != '':
        posts = BlogPost.objects.filter(category_id = request.GET.get('category'))
    else:
        posts= BlogPost.objects.all()
    categories = Category.objects.all()
    return render(request, 'blogList.html', {'posts':posts, 'categories':categories})



def blogDetail_Page(request, id):
    blogDetail = BlogPost.objects.get(pk=id)
    return render(request, 'blogDetail.html', {'blogDetail':blogDetail})


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



def editDraft(request, id):
    if request.user.is_authenticated and UserProfile.objects.filter(username=request.user).first().designation == 'doctor':
        categories = Category.objects.all()
        draft = Draft.objects.filter(pk=id).first()
        return render(request, 'createDraft.html', {'categories': categories, 'draft':draft})
    else:
        return redirect('blogList')
    


def draftList(request):
    if request.method == 'GET' and len(request.GET)>0 and request.GET.get('category') != '':
        posts = Draft.objects.filter(category_id = request.GET.get('category'))
    else:
        posts= Draft.objects.all()
    categories = Category.objects.all()
    return render(request, 'draftList.html', {'posts':posts, 'categories':categories})