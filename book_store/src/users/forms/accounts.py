from src.users.models import User, Address
from django import forms

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def clean(self):
        print('clean')
        cleaned_data = super().clean()
        print("email", cleaned_data.get('email'))
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
    
    def save(self, commit=True):
        print('save')
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number']

    def save(self, *args, **kwargs):
        print('save')
        print('new data', self.cleaned_data)
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save(update_fields=['email', 'username', 'first_name', 'last_name', 'phone_number'])
        return user
    
    def clean(self):
        print('clean')
        cleaned_data = super().clean()
        print('cleaned_data', cleaned_data)
        return cleaned_data
    

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'city', 'district', 'ward', 'street', 'note']
    
    def save(self, *args, **kwargs):
        print('save')
        address = super().save(commit=False)
        address.address = self.cleaned_data['address']
        address.city = self.cleaned_data['city']
        address.district = self.cleaned_data['district']
        address.ward = self.cleaned_data['ward']
        address.street = self.cleaned_data['street']
        address.note = self.cleaned_data['note']
        address.save(update_fields=['address', 'city', 'district', 'ward', 'street', 'note'])
        return address
    
    

