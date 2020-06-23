from allauth.account.forms import LoginForm, SignupForm
from django import forms

from .models import User


class RegisterUserForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label=("Username"),

                                                  widget=forms.TextInput(
                                                      attrs={'placeholder':
                                                                 ('Username'),
                                                             }))
        self.fields['email'].widget = forms.EmailInput(
            attrs={'type': 'email', 'class': 'form-control', 'placeholder': "Email address",
                   'id': 'inputEmail'})
        self.fields['username'].widget = forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': "Username", 'id': 'inputUsername'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': "Password", 'id': 'inputPassword1'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': "form-control", 'placeholder': "Confirm password", 'id': 'inputPassword2'})

        # def save(self, request):
        #     # Ensure you call the parent class's save.
        #     # .save() returns a User object.
        #     user = super().save(request)
        #
        #
        #     # Add your own processing here.
        #
        #     # You must return the original result.
        #     return user

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()
        return user


class LoginUserForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(
            attrs={'type': 'email', 'class': 'form-control', 'placeholder': "Email address", 'id': 'inputEmail'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': "form-control", 'placeholder': "Password", 'id': 'inputPassword'})

        def login(self, *args, **kwargs):
            return super().login(*args, **kwargs)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image', 'firstname', 'lastname', 'username', 'description', )
        labels = {
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'username': 'Username',
            'description': 'About you',
            #
            'image': 'Photo',
        }
        widgets = {
            'firstname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'FirstnameId',
                    'label': 'First name',
                    'placeholder': 'Enter you name'

                }
            ),
            'lastname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'LastnameId',
                    'label': 'Last Name',
                    'placeholder': 'Enter you lastname'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'UsernameId',
                    'label': 'Username',
                    'placeholder': 'Enter you username'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'DescriptionId',
                    'label': 'Username',
                    'placeholder': 'Write something about yorself (e.g. your interests, job, professional skills, etc)'
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'type': "file",
                    'class': "form-control-file",
                    'id': "FileId",

                })
        }


    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                user = User.objects.exclude(pk=self.instance.pk).filter(username=username).get()

            except User.DoesNotExist:
                return username
            raise forms.ValidationError('Username {} already exists. Please, select another one'.format(username))

