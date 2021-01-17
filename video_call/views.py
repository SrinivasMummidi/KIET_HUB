from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from events.forms import UpdatesForm
from django.http import HttpResponse, JsonResponse
from events.models import Updates


@login_required
def VideoCall(request):
	context = {}
	context['title'] = 'Conference'
	form = UpdatesForm()
	if request.method == 'POST':
		form = UpdatesForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse('')
	else:
		context['form']=form		
		return render(request, 'video.html',context)