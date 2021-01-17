from django.db import models
from django.utils import timezone
from users.models import User, UserGroup
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Task(models.Model):
	title = models.CharField(max_length=100)
	headline = models.CharField(max_length=100,default='')
	task_info =  RichTextUploadingField()
	date_posted = models.DateTimeField(default=timezone.now)
	assigned_by = models.ForeignKey(User, on_delete=models.SET('admin'))
	access = models.ManyToManyField(UserGroup)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('task-detail', kwargs={'pk': self.pk})

class TaskResponse(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	response = RichTextUploadingField(config_name='response')
	response_time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.username+'/'+self.task.title