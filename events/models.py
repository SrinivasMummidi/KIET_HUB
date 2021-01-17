from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
from users.models import UserGroup, User
from ckeditor.fields import RichTextField


def weekend():
		return timezone.now()+timedelta(weeks=1)

class Updates(models.Model):
	title = models.CharField(max_length=30)
	content = RichTextField(config_name='response')
	access = models.ManyToManyField(UserGroup)
	date_posted = models.DateTimeField(default=timezone.now)
	end = models.DateTimeField(default=weekend)


	def __str__(self):
		return f'{self.title}'
	
class Event(models.Model):
	title = models.CharField(max_length=50)
	event_image = models.ImageField(default='events.jpg',upload_to='event_pics')
	headline = models.TextField(default='')
	information = RichTextField()
	date_posted = models.DateTimeField(default=timezone.now)
	editor = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)



	def __str__(self):
		return f'{self.title}'