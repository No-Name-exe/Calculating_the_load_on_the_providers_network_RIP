from django.shortcuts import render, redirect
from .models import Router, Application, AddedRouter
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import datetime
from django.db import connection
# Create your views here.

from django.http import HttpResponse
# Database={}
# Database["data"]={
# 		'routers': [
# 			{'img':'1.png','title': 'Маршрутизатор провайдера','desc':'Роутер TP-Link Archer C7 — высокопроизводительный роутер с поддержкой Gigabit Ethernet и мощным процессором', 'id': 1},
# 			{'img':'2.png','title': 'Маршрутизатор промежуточный','desc':'Роутер Asus RT-AC66U — надёжный роутер среднего класса с двумя диапазонами и функцией Mesh.', 'id': 2},
# 			{'img':'3.png','title': 'Маршрутизатор жилого дома','desc':'Роутер D-Link DIR-615 — компактный и недорогой роутер для домашнего использования с базовыми функциями', 'id': 3},
# 			{'img':'4.jpg','title': 'Маршрутизатор запасной','desc':'Роутер Netgear R6220 — резервный роутер с простым управлением и стабильной работой.', 'id': 4},
# 			{'img':'5.png','title': 'Маршрутизатор школы','desc':'Роутер Cisco RV340 — корпоративное устройство с усиленной безопасностью и поддержкой VPN.', 'id': 5},
# 			{'img':'6.jpg','title': 'Маршрутизатор почты','desc':'Роутер MikroTik hAP ac2 — роутер со встроенным файерволом и возможностями контроля трафика.', 'id': 6},
# 		]
# 	}

# Application={}
# Application = {
# 	"ListOfApplic": [
# 		{
# 			"id": "3",
# 			"ListRouter": [
# 				{"id": 1, "master": None, "load": "20%"},   # главный роутер в сети, у него нет мастера
# 				{"id": 3, "master": 1, "load": "20%"},
# 				{"id": 5, "master": 3, "load": "20%"},
# 			],
# 			"network_load": "75%",
# 			"total_users": 150,
# 			"address": "ул. Ленина, д. 10"
# 		},
# 		{
# 			"id": "5",
# 			"ListRouter": [
# 				{"id": 3, "master": None, "load": "20%"},
# 				{"id": 4, "master": 3, "load": "20%"},
# 			],
# 			"network_load": "60%",
# 			"total_users": 90,
# 			"address": "школа №7"
# 		},
# 	]
# }

# Константы и параметры по умолчианию
defaul_application_id=3

def GetRouters(request, application_routers_id=defaul_application_id):
	context = {}
	context.update({'ListOfApplic': Application.objects.get(id=application_routers_id)})    # добавляем ключи из Application
	context.update({'ListRouter': AddedRouter.objects.filter(id_application=application_routers_id)})    # добавляем ключи из Application
	context['default'] = {
		'application': {
			'id': application_routers_id
		}
	}

	input_text = request.POST.get("search")
	if input_text is not None:
		final=Router.objects.filter(title__startswith=input_text).order_by('id')
	else:
		final=Router.objects.all()
	context.update({'data' : {'routers': final}})
	# if input_text is not None:
	# 	context.update({'data' : {'req': input_text}})
	return render(request, 'selection.html', context)

def GetRouter(request, id):
	Looking=id
	print(Router.objects.get(id=Looking))
	return render(request, 'router.html', {'data' :Router.objects.get(id=Looking)})

def GetApplicationRouter(request, id=0):

	if id==0:
		try:
			ApplicationFound=Application.objects.get(creator=request.user, status='черновик')
		except ObjectDoesNotExist:
			print("bad")
			return redirect(request.META.get('HTTP_REFERER'))
		else:
			print("good")
			pass

	else:
		request_id=id
		ApplicationFound=Application.objects.get(id=request_id)
		if ApplicationFound.status=="удалено":
			return redirect('sendSearch')
		return render(request, 'application.html', {'id': ApplicationFound.id, 'address': ApplicationFound.Adress, 'total_users': ApplicationFound.TotalUsers, 'data' : {'routers': AddedRouter.objects.filter(id_application=ApplicationFound.id) } })



def AddRouterDatabase(request, id):
	request_id = request.POST.get("router_id")
	if request.POST.get("update_app"):
		request_id= request.POST.get("application_id")
		print(request_id)
		if request.POST.get("Adress") !='': request_Adress = request.POST.get("Adress") 
		else: request_Adress=''
		if request.POST.get("TotalUsers") !='': request_TotalUsers = request.POST.get("TotalUsers")
		else: request_TotalUsers=None
		Application.objects.filter(id=request_id).update(Adress=request_Adress, TotalUsers=request_TotalUsers)
		
		return redirect('application_router_url', request_id)
	
	elif request.POST.get("update_router"):
		if request.POST.get("Master") !='': request_Master = request.POST.get("Master") 
		else: request_Master=''
		if request.POST.get("Load") !='': request_Load = request.POST.get("Load") 
		else: request_Load=''
		AddedRouter.objects.filter(id_application=request_id, id_router=Router.objects.get(id=request_id)).update(master_router_id=request_Master, router_load=request_Load)
		
	else:

		print(request_id)
		# При отстутствии заявки в статусе черновик у пользователя, она создается только при добавлении услуги в заявку. Если такая заявка уже есть, то услуга добавляется сразу в нее. Удаленные заявки просматривать нельзя, если у пользователя нет текущей заявки, ее карточка на странице услуг не активна.
		try:
			ApplicationFound=Application.objects.get(creator=request.user, status='черновик')
			
		except ObjectDoesNotExist:
			Application.objects.create(creator=request.user, status='черновик', date_create=datetime.now().date())
			AppFound=Application.objects.get(creator=request.user, status='черновик')
			AddedRouter.objects.create(id_application=AppFound, id_router=Router.objects.get(id=request_id))
			return redirect('phenom_selection_url')
		except MultipleObjectsReturned:
			print("Несколько черновиков")
			pass
		else:
			AddedRouter.objects.create(id_application=ApplicationFound, id_router=Router.objects.get(id=request_id))
			return redirect('application_router_url', id=ApplicationFound.id)
	redirect('application_router_url')

def DeleteStatusApplicationRouterDatabase(request, id):
	target = request.POST.get("application_id")
	Application.objects.update(date_end=datetime.now().date())
	print(target)
	with connection.cursor() as cursor:
		cursor.execute("UPDATE Application SET status = 'удалено' WHERE id = %s", [id])
	return redirect('sendSearch')