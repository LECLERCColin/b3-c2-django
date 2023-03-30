from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from resaInterface.models import Course, School


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('school', 'title', 'description', 'image')
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CourseCreationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['school'].queryset = School.objects.filter(name=user.username)


# Logging form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, label='Nom d\'utilisateur')
    password = forms.CharField(max_length=200, widget=forms.PasswordInput, label='Mot de passe')


class RegisterForm(UserCreationForm):
    is_school = forms.BooleanField(required=False, label="Je suis une école", initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    school_image = forms.ImageField(required=False, label='Image de l\'école', widget=forms.FileInput(attrs={'class': 'form-control'}))
    school_address = forms.CharField(required=False, label='Adresse de l\'école', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    school_phone = forms.CharField(required=False, label='Téléphone de l\'école', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=200, label='Nom d\'utilisateur / Ecole', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Nom d\'utilisateur / Ecole'}))
    email = forms.EmailField(label='Adresse mail', widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'email@email.email'}))
    first_name = forms.CharField(label='Prénom', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Prénom'}))
    last_name = forms.CharField(label='Nom de famille', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Nom de famille'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            if self.cleaned_data['is_school']:
                self.create_school(user)
        return user

    def create_school(self, user):
        group = Group.objects.get(name='schools')
        user.groups.add(group)
        school = School(name=user.username, image=self.cleaned_data['school_image'], address=self.cleaned_data['school_address'], phone=self.cleaned_data['school_phone'])
        school.save()

