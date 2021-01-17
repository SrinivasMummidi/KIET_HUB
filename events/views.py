from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import UpdatesForm, EventsForm
from django.contrib.auth.decorators import login_required
from users.models import User
from .models import Updates, Event
from datetime import datetime
import pytz


class EventListView(LoginRequiredMixin, ListView):
	model = Event
	paginate_by = 2
	template_name = 'events/events.html'
	context_object_name='events'
	ordering = ['-date_posted']

	def get_context_data(self, **kwargs):
		context = super(EventListView, self).get_context_data(**kwargs)
		context['title'] = 'Events'
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
		return context

class EventDetailView(LoginRequiredMixin, DetailView):
	model = Event


class AddEvent(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Event
	form_class = EventsForm
	context_object_data = 'form'

	def get_context_data(self, **kwargs):
		context = super(AddEvent, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context

	def test_func(self):
		return self.request.user.is_staff

class UpdateEvent(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Event
	form_class = EventsForm
	context_object_data = 'form'

	def get_context_data(self, **kwargs):
		context = super(UpdateEvent, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context

	def test_func(self):
		return self.request.user.is_staff

class AddUpdate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Updates
	form_class = UpdatesForm
	context_object_data = 'form'

	def get_context_data(self, **kwargs):
		context = super(AddUpdate, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context

	def test_func(self):
		return self.request.user.is_staff

class UpdateUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Updates
	form_class = UpdatesForm
	context_object_data = 'form'

	def get_context_data(self, **kwargs):
		context = super(UpdateUpdate, self).get_context_data(**kwargs)
		context['title'] = 'Management'
		return context

	def test_func(self):
		return self.request.user.is_staff