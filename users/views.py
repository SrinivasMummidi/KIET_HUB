from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm, LeadershipCreateForm, TeamCreateForm, GroupForm
from django.contrib.auth.models import User, Group
from .models import Leadership, Team, User, UserProfile, UserGroup
import csv,io


def register(request):
	context = {'title':'Register'}
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			name = form.cleaned_data.get('username')
			messages.success(request,f'Account created for {name}')
			return redirect('Kiet-Login')
		else:
			context['form'] = form
	else:
		form = RegistrationForm()
		context['form'] = form
	return render(request, 'users/register.html', context)

@login_required	
def profile(request):
	context={'title':'Profile'}
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request,f'Your Account has been Updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.userprofile)
	context['u_form']=u_form
	context['p_form']=p_form
	return render(request, 'users/profile.html',context)

@login_required
def ManageUser(request):
	context={}
	context['title'] = 'Management'
	
	return render(request, 'users/usermanagment.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })

@login_required
def AddUser(request):
	if request.user.is_staff:
		context={}
		context['title'] = 'Management'
		context['format'] = 'username,email'
		if request.method == 'POST':
			csv_file = request.FILES['file']
			if not csv_file.name.endswith('csv'):
				messages.error(request,'This is not a csv file')
			else:
				data_set = csv_file.read().decode('UTF-8')
				io_string = io.StringIO(data_set)
				next(io_string)
				for column in csv.reader(io_string, delimiter=','):
					print(column)
					user, created = User.objects.update_or_create(
							username = column[0],
							email = column[1]
						)
					user.set_password('Demo@123')
					user.save()
				messages.success(request,f'Users Updated!')
		return render(request, 'users/add_user.html', context)
	else:
		return redirect('Kiet-Home')

@login_required
def AddStaff(request):
	if request.user.is_staff:
		context={}
		context['title'] = 'Management'
		context['format'] = 'username,email'
		if request.method == 'POST':
			csv_file = request.FILES['file']
			if not csv_file.name.endswith('csv'):
				messages.error(request,'This is not a csv file')
			else:
				data_set = csv_file.read().decode('UTF-8')
				io_string = io.StringIO(data_set)
				next(io_string)
				for column in csv.reader(io_string, delimiter=','):
					print(column)
					user, created = User.objects.update_or_create(
							username = column[0],
							email = column[1],
							is_staff = True
						)
					user.set_password('Kiet@123')
					user.save()
					group = Group.objects.get(name='Staff')
					user.groups.add(group)
				messages.success(request,f'Staff Updated!')
		return render(request, 'users/add_staff.html', context)
	else:
		return redirect('Kiet-Home')

class AddLeadership(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Leadership
	form_class = LeadershipCreateForm
	success_url = 'Manage-User/'
	context_object_data = 'form'
	def get_context_data(self, **kwargs):
		context = super(AddLeadership, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context
	
	def test_func(self):
		if self.request.user.is_staff:
			return True
		return False

class UpdateLeadership(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Leadership
	form_class = LeadershipCreateForm
	success_url = 'Manage-User/'
	context_object_data = 'form'
	def get_context_data(self, **kwargs):
		context = super(UpdateLeadership, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context
	
	def test_func(self):
		return self.request.user.is_staff


class AddTeam(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Team
	form_class = TeamCreateForm
	success_url = 'Manage-User/'
	context_object_data = 'form'
	def get_context_data(self, **kwargs):
		context = super(AddTeam, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context

	def test_func(self):
		return self.request.user.is_staff

class UpdateTeam(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Team
	form_class = TeamCreateForm
	success_url = 'Manage-User/'
	context_object_data = 'form'
	def get_context_data(self, **kwargs):
		context = super(UpdateTeam, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context

	def test_func(self):
		return self.request.user.is_staff

class CreateGroup(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = UserGroup
	form_class = GroupForm
	context_object_data = 'form'

	def test_func(self):
		return self.request.user.is_staff

	def get_context_data(self, **kwargs):
		context = super(CreateGroup, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context


class UpdateGroup(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = UserGroup
	form_class = GroupForm
	context_object_data = 'form'

	def get_context_data(self, **kwargs):
		context = super(UpdateGroup, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context

	def test_func(self):
		return self.request.user.is_staff
