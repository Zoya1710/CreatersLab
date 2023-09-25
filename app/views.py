
from django.shortcuts import render , HttpResponse , redirect
from app.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth  import authenticate,  login, logout
from .forms import DocumentForm
# Create your views here.
def app(request):
    return render(request,'home.html')

def contact(request):
    if request.method=='POST' and request.FILES['upload']:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        form = DocumentForm(request.POST, request.FILES)
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        
        print(name, email, phone, content, form)
        contact = Contact(name=name, email=email, phone=phone, content=content, form=form)
        contact.save()
        
        
        
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content, form=form)
            contact.save()
            messages.success(request,"Your message has been send successfully")
    return render(request, 'contact.html')


def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        
        
        if len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('app')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('app')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('app')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('app')

    else:
        return HttpResponse("404 - Not found")
    
def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("app")
        else:
            messages.error(request, "Invalid Credentials! Please try again")
            return redirect("app")

    return HttpResponse("404- Not found")
   
    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('app')