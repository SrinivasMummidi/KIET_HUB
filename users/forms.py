from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User,UserProfile,Leadership, Team, UserGroup


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60,help_text='Required. Enter a valid Email address')

	class Meta:
		model = User
		fields = ('username','email','password1','password2')

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(help_text='Required. Enter a valid Email address')
	class Meta:
		model = User
		fields = ('first_name','last_name','username','email')

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('college','branch','year','image')

class LeadershipCreateForm(forms.ModelForm):
	class Meta:
		model = Leadership
		fields = '__all__'

class TeamCreateForm(forms.ModelForm):
	# team = forms.MultipleChoiceField(queryset=User.objects.filter(userprofile__year=user.userprofile.year,userprofile__branch=user.userprofile.branch))
	class Meta:
		model = Team
		fields = '__all__'


class GroupForm(forms.ModelForm):

	class Meta:
		model = UserGroup
		fields = '__all__'

