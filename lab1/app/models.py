from django.db import models

# Create your models here.

class Application(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'черновик'
		DELETED = 'удалено'
		FORMULATED = 'сформирован'
		COMPLETED = 'завершён'
		REJECTED = 'отклонён'

	# id = models.IntegerField(primary_key=True)
	creator = models.CharField(max_length=255)
	moderator = models.CharField(max_length=255,null=True,blank=True)
	status = models.CharField(max_length=255, choices=Status.choices, default=Status.DRAFT)
	date_create = models.DateField()
	date_modific= models.DateField(null=True,blank=True)
	date_end= models.DateField(null=True,blank=True)
	Adress= models.CharField(max_length=255,null=True)
	TotalUsers= models.IntegerField(null=True,blank=True)


	class Meta:
		db_table = 'application'
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
	status = models.CharField(max_length=255,null=True,blank=True)
	# id = models.AutoField(primary_key=True)
	
	class Meta:
		db_table = 'router'
		app_label = 'app'
	
	def __str__(self):
		return self.title

class AddedRouter(models.Model):
	id_application = models.ForeignKey(Application, on_delete=models.PROTECT, default=1)
	id_router = models.ForeignKey(Router, on_delete=models.PROTECT, default=1)
	master_router_id = models.IntegerField(null=True,blank=True)
	router_load = models.CharField(max_length=255,null=True,blank=True)

	class Meta:
		db_table = 'addedrouter'
		app_label = 'app'