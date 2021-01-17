from django.db import models
from django.contrib.auth.models import User
from PIL import Image

def get_username(self):
    return self.username

User.add_to_class("__str__", get_username)

class UserProfile(models.Model):
	user = 				models.OneToOneField(User,on_delete=models.CASCADE)
	image = 			models.ImageField(default='default.jpg',upload_to='profile_pics')
	last_login = 		models.DateTimeField(auto_now=True)
	BRANCH_CHOICES = 	[('', '-----'),('ECE','Electronics & Communication Engineering'),('CSE','Computer Science Engineering'), ('MECH','Mechanical Engineering'),('CIV','Civil Engineering'),('EEE', 'Electrical Engineering')]
	branch = 			models.CharField(max_length=10,choices=BRANCH_CHOICES,default='')
	COLLEGE_CHOICES = 	[('', '-----'),('Kiet','Kiet'),('Kiek','Kiet+'),('Kietw','KietW')]
	college = 			models.CharField(max_length=10,choices=COLLEGE_CHOICES,default='')
	YEAR_CHOICES = 		[(0, '-----'),(1,'I'),(2,'II'),(3,'III'),(4,'IV')]
	year =				models.IntegerField(choices=YEAR_CHOICES,default=0)
	is_leader = 		models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user.username}'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)

class UserGroup(models.Model):
	name = models.CharField(max_length=50)
	users = models.ManyToManyField(User)

	def __str__(self):
		return f'{self.name}'

class Leadership(models.Model):
	team_id = models.CharField(max_length=20)
	leader = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.team_id}'

class Team(models.Model):
	leader = models.OneToOneField(Leadership,on_delete=models.CASCADE)
	team = models.ManyToManyField(User)


	def __str__(self):
		return f'{self.leader}'
