from django.shortcuts import render, redirect, get_object_or_404
from .models import Router, ApplicationRouter, AddedRouter
from django.contrib.auth.models import User
from .minio import Minio_addpicture, Minio_deletepicture
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import datetime
from django.db import connection

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import RouterSerializer, AppSerializer, AddedSerializer, UserDetailSerializer
from rest_framework.response import Response


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

	try:
		application_routers_id=ApplicationRouter.objects.get(creator=request.user, status='черновик').id
	except ObjectDoesNotExist:
		context.update({'ListOfApplic': ""})    # добавляем ключи из Application
		context.update({'ListRouter': ""})    # добавляем ключи из Application
		pass
	except MultipleObjectsReturned:
		print("Несколько черновиков")
		pass
	else:
		context.update({'ListOfApplic': ApplicationRouter.objects.get(id=application_routers_id)})    # добавляем ключи из Application
		context.update({'ListRouter': AddedRouter.objects.filter(id_application=application_routers_id)})    # добавляем ключи из Application
		pass
	
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
			ApplicationFound=ApplicationRouter.objects.get(creator=request.user, status='черновик')
		except ObjectDoesNotExist:
			print("bad")
			return redirect(request.META.get('HTTP_REFERER'))
		else:
			print("good")
			pass

	else:
		request_id=id
		ApplicationFound=ApplicationRouter.objects.get(id=request_id)
		if ApplicationFound.status=="удалено":
			return redirect('sendSearch')
		def TreeCreate(data):
			lookup = {}
			for node in data:
				node['children'] = []
				lookup[node['id']] = node

			roots = []
			for node in data:
				parent_id = node['master_router_id']
				if parent_id:
					parent = lookup.get(parent_id)
					if parent:
						parent['children'].append(node)
				else:
					roots.append(node)
			return roots
			
		TreeData=TreeCreate(list(AddedRouter.objects.filter(id_application=ApplicationFound.id).values()))
		return render(request, 'application.html', {'id': ApplicationFound.id, 'address': ApplicationFound.Adress, 'total_users': ApplicationFound.TotalUsers, 'data' : {'routers': AddedRouter.objects.filter(id_application=ApplicationFound.id) }, 'tree' : TreeData})



def AddRouterDatabase(request, id):
	request_id = request.POST.get("router_id")
	if request.POST.get("update_app"):
		request_app= request.POST.get("application_id")
		request_routers=request.POST.getlist('router_id[]')
		request_masters = request.POST.getlist('Master[]')
		request_loads = request.POST.getlist('Load[]')
		
		print(request_app)
		if request.POST.get("Adress") !='': request_Adress = request.POST.get("Adress") 
		else: request_Adress=''
		if request.POST.get("TotalUsers") !='': request_TotalUsers = request.POST.get("TotalUsers")
		else: request_TotalUsers=None
		ApplicationRouter.objects.filter(id=request_app).update(Adress=request_Adress, TotalUsers=request_TotalUsers)
		
		for RouterTarget, MasterTarget, LoadTarget in zip(request_routers, request_masters, request_loads):
			if RouterTarget==MasterTarget:
				print("Ошибка совпадает роуетер с назначаемым мастером")
			else:
				AddedRouter.objects.filter(id=RouterTarget).update(master_router_id=MasterTarget or None, router_load=LoadTarget or '')

		return redirect('application_router_url', request_app)
	
	elif request.POST.get("update_router"):
		pass
		
	else:

		print(request_id)
		# При отстутствии заявки в статусе черновик у пользователя, она создается только при добавлении услуги в заявку. Если такая заявка уже есть, то услуга добавляется сразу в нее. Удаленные заявки просматривать нельзя, если у пользователя нет текущей заявки, ее карточка на странице услуг не активна.
		try:
			ApplicationFound=ApplicationRouter.objects.get(creator=request.user, status='черновик')
			
		except ObjectDoesNotExist:
			ApplicationRouter.objects.create(creator=request.user, status='черновик', date_create=datetime.now().date())
			AppFound=ApplicationRouter.objects.get(creator=request.user, status='черновик')
			AddedRouter.objects.create(id_application=AppFound, id_router=Router.objects.get(id=request_id))
			return redirect('sendSearch')
		except MultipleObjectsReturned:
			print("Несколько черновиков")
			pass
		else:
			AddedRouter.objects.create(id_application=ApplicationFound, id_router=Router.objects.get(id=request_id))
			return redirect('sendSearch')
			# return redirect('application_router_url', id=ApplicationFound.id)
	redirect('application_router_url')

def DeleteStatusApplicationRouterDatabase(request, id):
	target = request.POST.get("application_id")
	ApplicationRouter.objects.update(date_end=datetime.now().date())
	print(target)
	with connection.cursor() as cursor:
		cursor.execute("UPDATE ApplicationRouter SET status = 'удалено' WHERE id = %s", [id])
	return redirect('sendSearch')


#REST API
#▼▼▼▼▼▼▼▼

def user():
	try:
		user1 = User.objects.get(id=1)
	except:
		pass
	return user1

#Домен услуги:
class StockList(APIView):
	model_class = Router
	serializer_class = RouterSerializer

@api_view(['GET'])
def GetRecord(request, id, format=None):
	Router_instance = get_object_or_404(Router, id=id)
	serializer = RouterSerializer(Router_instance)
	return Response(serializer.data)
@api_view(['GET'])
def GetFilter(request, search, format=None):
	Router_list = Router.objects.filter(title__startswith=search)
	serializer = RouterSerializer(Router_list, many=True)
	return Response(serializer.data)
@api_view(['POST'])
def PostRouter(request, format=None):
	serializer = RouterSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def PutRouter(request, id, format=None):
	Router_list = get_object_or_404(Router, id=id)
	serializer = RouterSerializer(Router_list, data=request.data, partial=True)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def DeleteRouter(request, id, format=None):
	Router_instance = get_object_or_404(Router, id=id)
	Router_instance.delete()
	Minio_deletepicture(id)
	return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
def PostDraft(request, id, format=None):
	Router_instance = get_object_or_404(Router, id=id)

	application = ApplicationRouter.objects.create(
	creator=user(),
	date_create=datetime.now().date(),
	status=ApplicationRouter.Status.DRAFT
	)

	AddedRouter.objects.create(
	id_application=application,
	id_router=Router_instance
	)

	serializer = AppSerializer(application, data=request.data)
	print(serializer)
	if serializer.is_valid():
		# serializer.save()
		serializer.creator=user()
		print(serializer)
	return Response(status=status.HTTP_201_CREATED)
@api_view(['POST'])
def PostPicture(request, id, format=None):
	print("Request data:", request.data)
	print("Request FILES:", request.FILES)

	Router_instance = get_object_or_404(Router, id=id)

	pic = request.FILES.get('img')
	if not pic:
		return Response({"error": "Файл не прикреплен"}, status=status.HTTP_400_BAD_REQUEST)
	
	pic_result = Minio_addpicture(Router_instance, pic)
	if 'error' in pic_result:
		return pic_result
	
	serializer = RouterSerializer(Router_instance)
	# if serializer.is_valid():
	# 	serializer.save()
	# 	return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.data, status=status.HTTP_201_CREATED)

#Домен заявки:
@api_view(['GET'])
def GetIcons():
	pass
@api_view(['GET'])
def GetApps():
	pass
@api_view(['GET'])
def GetApp():
	pass
@api_view(['PUT'])
def PutApp():
	pass
@api_view(['PUT'])
def PutComplete():
	pass
@api_view(['PUT'])
def PutModerator():
	pass
@api_view(['DELETE'])
def DeleteApp():
	pass

#Домен м-м:
@api_view(['DELETE'])
def DeleteAdded():
	pass
@api_view(['PUT'])
def PutAdded():
	pass

#Домен пользователь:
@api_view(['POST'])
def PostRegister():
	pass
@api_view(['GET'])
def GetUser():
	pass
@api_view(['PUT'])
def PutUser():
	pass
@api_view(['POST'])
def PostAuth():
	pass
@api_view(['POST'])
def PostExit():
	pass