from django.shortcuts import render, redirect
from src.users.models import User, Address
from src.users.forms.accounts import CustomUserCreationForm, UserProfileUpdateForm, AddressForm
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

User = get_user_model()


class UserCreateView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = '/users/login/'
    

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
        
    

# Login View
class LoginViewCustom(TemplateView):
    template_name = 'users/login.html'
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        message = 'Invalid credentials'
        print(message)
        return render(request, self.template_name, {'message': message})
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    

# Profile View
class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
        
    def post(self, request, *args, **kwargs):
        type_form = request.POST.get('type')
        user = request.user
        address = Address.objects.filter(user=user).first()
        # check user has address
        if not address:
            address = Address(user=user)
            address.save()
        
        profile_form = UserProfileUpdateForm(request.POST, instance=user)
        address_form = AddressForm(request.POST, instance=address)
        if type_form == 'profile':
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
            else:
                print(profile_form.errors)
        elif type_form == 'address':
            if address_form.is_valid():
                address_form.save()
                return redirect('profile')
            else:
                print(address_form.errors)
        return render(request, self.template_name)
    
    
    def get(self, request, *args, **kwargs):
        user = request.user
        address = Address.objects.filter(user=user).first()
        return render(request, self.template_name, {'user': user, 'address': address})


    
# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')
