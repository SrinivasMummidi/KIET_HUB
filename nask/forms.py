from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Task, TaskResponse

class TaskForm(forms.ModelForm):
    task_info = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Task
        fields = ('title','headline','task_info','access')

class ResponseForm(forms.ModelForm):
	response = forms.CharField(widget=CKEditorUploadingWidget(config_name='response'))
	class Meta:
		model = TaskResponse
		fields = ('response',)