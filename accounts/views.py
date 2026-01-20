from django.shortcuts import render,redirect
import stripe
from django.conf import settings
from django.contrib.auth import login,logout,update_session_auth_hash
from django.views import View
from accounts.forms import ProfileForm,registerform
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm


# Create your views here.
@login_required(login_url='account:login')
def logout_view(request):
    logout(request)
    return redirect('account:login')    

class LoginView(View):
    def get(self,request,*args, **kwargs):
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})

    def post(self,request,*args, **kwargs):
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('base:home')
        else:
            return render(request,'login.html',{'form':form,'invalid':'invalid username or password'})

class CreatePfpView(View):
    def get(self,request,*args, **kwargs):
        form=ProfileForm()
        return render (request,'create_pfp.html',{'form':form})
    
    def post(self,request,*args, **kwargs):
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect('account:account')
        else:
            form=ProfileForm()
            return render(request,'create_pfp.html',{'form':form,'invalid':'Something went wrong'})

class UpdatePfpView(View):
    def get(self,request,*args, **kwargs):
        data=request.user.profile
        form=ProfileForm(instance=data)
        return render(request,'create_pfp.html',{'form':form})

    def post(self,request,*args, **kwargs):
        data=request.user.profile
        form=ProfileForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            return redirect('account:account')
        return render(request,'create_pfp.html',{'form':form})

class MyaccountView(View):
    @method_decorator(login_required(login_url='account:login'))
    def get(self,request,*args, **kwargs):
        return render (request,'account.html')

class PasswordChangeView(View):
    def get(self,request,*args, **kwargs):
        form=PasswordChangeForm(user=request.user)
        return render(request,'password_change.html',{'form':form})

    def post(self,request,*args, **kwargs):
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            update_session_auth_hash(request,form.user)
            form.save()
            return redirect('account:account')
        return render(request,'password_change.html',{'form':form})

stripe.api_key =settings.STRIPE_SECRET_KEY

class RegisterView(View):
    def get(self,request,*args, **kwargs):
        form=registerform()
        return render(request,'registration.html',{'form':form})
    
    def post(self,request,*args, **kwargs):
        form=registerform(request.POST)
        if form.is_valid():
            user = stripe.Customer.create(
            email=form.cleaned_data.get('email'),
            )
            customer=form.save(commit=False)
            customer.stripe_customer_id=user.id
            customer.save()
            return redirect('account:login')
        else:
            return render(request,'registration.html',{'form':form})