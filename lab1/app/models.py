from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ApplicationRouter(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'черновик'
		DELETED = 'удалено'
		FORMULATED = 'сформирован'
		COMPLETED = 'завершён'
		REJECTED = 'отклонён'

	# id = models.IntegerField(primary_key=True)
	creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="applications_created")
	moderator = models.ForeignKey(User, on_delete=models.PROTECT, null=True,blank=True, related_name="applications_moderated")
	status = models.CharField(max_length=255, choices=Status.choices, default=Status.DRAFT)
	date_create = models.DateField()
	date_modific= models.DateField(null=True,blank=True)
	date_end= models.DateField(null=True,blank=True)
	Adress= models.CharField(max_length=255,null=True)
	TotalUsers= models.IntegerField(null=True,blank=True)


	class Meta:
		db_table = 'applicationrouter'
		app_label = 'app'
	
	def __str__(self):
		return f"Заявка	 № {self.id}"

		
class Router(models.Model):
	class Status(models.TextChoices):
		DELETED = 'удалено'
		EXIST = 'действует'

	title = models.CharField(max_length=30)
	desc = models.CharField(max_length=255)
	img = models.CharField(max_length=255,null=True,blank=True)
	status = models.CharField(max_length=255, choices=Status.choices, default=Status.EXIST)
	# id = models.AutoField(primary_key=True)
	
	class Meta:
		db_table = 'router'
		app_label = 'app'
	
	def __str__(self):
		return self.title

class AddedRouter(models.Model):
	id_application = models.ForeignKey(ApplicationRouter, on_delete=models.PROTECT, default=1)
	id_router = models.ForeignKey(Router, on_delete=models.PROTECT, default=1)
	master_router_id = models.IntegerField(null=True,blank=True)
	router_load = models.CharField(max_length=255,null=True,blank=True)

	class Meta:
		db_table = 'addedrouter'
		app_label = 'app'