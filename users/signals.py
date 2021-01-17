from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import UserProfile, UserGroup, Leadership, Team


@receiver(post_save,sender=User)
def create_userprofile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
	instance.userprofile.save()

@receiver(post_save,sender=User)
def save_userprofile(sender, instance, created, **kwargs):
	instance.userprofile.save()

@receiver(post_save,sender=UserProfile)
def connect(sender, instance, created, **kwargs):
	if instance.branch!= '' and instance.year!=0 and instance.college!='':
		group = str(instance.year)+'_'+instance.branch+'_'+instance.college
		if(UserGroup.objects.filter(name=group)):
			if instance.user not in list(UserGroup.objects.filter(name=group).first().users.all()):
				UserGroup.objects.filter(name=group).first().users.add(instance.user)
		else:
			UserGroup.objects.create(name=group)
			UserGroup.objects.filter(name=group).first().users.add(instance.user)

@receiver(post_save,sender=Leadership)
def create_leader_group(sender, instance, created, **kwargs):
	name = instance.team_id
	u = UserProfile.objects.filter(user=instance.leader).first()
	u.is_leader = True
	group = Group.objects.get(name="Leader")
	u.save()
	instance.leader.groups.add(group)
	if(not UserGroup.objects.filter(name=name).first()):
		UserGroup.objects.create(name=name)
		UserGroup.objects.filter(name=name).first().users.add(instance.leader)
	else:
		ug = UserGroup.objects.filter(name=name).first()
		for EVM in list(ug.users.all()):
			if(EVM.userprofile.is_leader):
				ug.users.remove(EVM)
		ug.users.add(instance.leader)
		ug.save()

@receiver(post_save,sender=Team)
def update_leader_group(sender, instance, created, **kwargs):
	name = instance.leader.team_id
	if(UserGroup.objects.filter(name=name).first()):
		UserGroup.objects.filter(name=name).first().delete()
	if(not UserGroup.objects.filter(name=name).first()):
		UserGroup.objects.create(name=name)
	ug = UserGroup.objects.filter(name=name).first()
	team = Team.objects.filter(leader__team_id=name).first()
	tm = list(team.team.all())
	for evm in tm:
		print(evm,tm)
		if(evm not in list(ug.users.all())):
			ug.users.add(evm)
		ug.save()
	ug = UserGroup.objects.filter(name=name).first()
	ug.save()
