from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task, TaskResponse
from users.models import Leadership
from datetime import datetime
import pytz
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import TaskForm, ResponseForm
from events.models import Updates

# Create your views here.
@login_required
def home(request):
	return redirect('Kiet-Login')

class TaskListView(LoginRequiredMixin, ListView):
	model = Task
	template_name = 'nask/tasks.html'
	context_object_name='tasks'
	paginate_by = 10
	task_set = None
	def dispatch(self, request, *args, **kwargs):
		if request.user.userprofile.branch == '':
			return redirect('profile')
		else:
			return super(TaskListView, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		 global task_set
		 task_set=Task.objects.filter(access__in=list(self.request.user.usergroup_set.all())).distinct().order_by('-date_posted')

		 return task_set

	def get_context_data(self, **kwargs):
		context = super(TaskListView, self).get_context_data(**kwargs)
		context['title'] = 'Tasks'
		updates = []
		ug = list(self.request.user.usergroup_set.all())
		for EVU in ug:
			if(EVU.updates_set.all()):
				updates.extend(list(EVU.updates_set.all().distinct()))
		utc = pytz.UTC
		def time():
			return utc.localize(datetime.now())
		for update in updates:
			if(time() >= update.end):
				update.delete()
		def u_sort(update):
			return update.date_posted
		context['updates'] = sorted(updates,key=u_sort,reverse=True)	
		completed = []
		pending = []
		for evt in list(set(task_set)):
			if(evt.taskresponse_set.filter(user=self.request.user).first()):
				completed.append(evt)
			else:
				pending.append(evt)
		context['pending'] = sorted(pending,key=u_sort,reverse=True)
		context['completed']= sorted(completed,key=u_sort,reverse=True)
		return context

@login_required
def TaskDetailView(request,pk):
	context = {}
	task = Task.objects.get(id=pk)
	response = TaskResponse.objects.filter(task=task,user=request.user).first()
	if response:
		form = ResponseForm(instance=response)
	else:
		form = ResponseForm()
	context['object']=task
	context['form'] = form
	if request.method == 'POST':
		if response:
			form = ResponseForm(request.POST, instance = response)
		else:
			form = ResponseForm(request.POST)
		context['form'] = form
		if form.is_valid():
			form.instance.user = request.user
			form.instance.task = task
			form.save()
			messages.success(request,f'Response Updated!')
	return render(request, 'nask/task_detail.html', context)
	
class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, FormView, CreateView):
	model = Task
	form_class = TaskForm

	def form_valid(self, form):
		form.instance.assigned_by = self.request.user
		return super().form_valid(form)

	def test_func(self):
		return self.request.user.is_staff

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, FormView, UpdateView):
	model = Task
	form_class = TaskForm

	def form_valid(self, form):
		form.instance.assigned_by = self.request.user
		return super().form_valid(form)

	def test_func(self):
		task = self.get_object()
		if self.request.user == task.assigned_by:
			return True
		return False

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Task
	success_url = '/'

	def test_func(self):
		task = self.get_object()
		if self.request.user == task.assigned_by:
			return True
		return False

@login_required
def ResponseListView(request,pk):
	if request.user.is_staff or request.user.userprofile.is_leader:
		context = {}
		task = Task.objects.get(id=pk)
		group_list = list(task.access.all())
		context['task'] = task
		context['leaders'] = Leadership.objects.filter(leader__userprofile__branch=request.user.userprofile.branch,leader__userprofile__year=request.user.userprofile.year)
		context['responses'] = TaskResponse.objects.filter(user__usergroup__in=group_list,task=task)
		return render(request, 'nask/taskresponse_list.html', context)
	else:
		redirect('task-detail')