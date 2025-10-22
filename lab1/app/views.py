from django.shortcuts import render, redirect
from .models import Router, ApplicationRouter, AddedRouter
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .minio import Minio_addpicture, Minio_deletepicture
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import datetime
from django.db import connection
from django.utils.dateparse import parse_datetime

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import RouterSerializer, AppSerializer, AddedSerializer, UserDetailSerializer, AppAddedRouterSerializer, UserRegisterSerializer, RouterPUTSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token


from rest_framework.request import Request
from django.http import HttpResponse, HttpRequest

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

def GetRouters(request: HttpRequest, application_routers_id=defaul_application_id):


	context = {}

	try:
		application_routers_id=ApplicationRouter.objects.get(creator=request.user, status='черновик')
	except ObjectDoesNotExist:
		context.update({'ListOfApplic': ""})    # добавляем ключи из Application
		context.update({'ListRouter': ""})    # добавляем ключи из Application
		pass
	except MultipleObjectsReturned:
		application_routers_id=ApplicationRouter.objects.filter(creator=request.user, status='черновик').first().pk # type: ignore
		context.update({'ListOfApplic': ApplicationRouter.objects.get(id=application_routers_id)})    # добавляем ключи из Application
		context.update({'ListRouter': AddedRouter.objects.filter(id_application=application_routers_id)})    # добавляем ключи из Application
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

def GetRouterHttp(request: HttpRequest, id):
	Looking=id
	print(Router.objects.get(id=Looking))
	return render(request, 'router.html', {'data' :Router.objects.get(id=Looking)})

def GetApplicationRouter(request: HttpRequest, id=0):

	if id==0:
		try:
			ApplicationFound=ApplicationRouter.objects.get(creator=request.user, status='черновик')
		except ObjectDoesNotExist:
			print("bad")
			return redirect(request.META.get('HTTP_REFERER') or 'sendSearch')
		else:
			print("good")
			return redirect(request.META.get('HTTP_REFERER') or 'sendSearch')

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
			
		TreeData=TreeCreate(list(AddedRouter.objects.filter(id_application=ApplicationFound.pk).values()))
		return render(request, 'application.html', {'id': ApplicationFound.pk, 'address': ApplicationFound.Adress, 'total_users': ApplicationFound.TotalUsers, 'data' : {'routers': AddedRouter.objects.filter(id_application=ApplicationFound.pk) }, 'tree' : TreeData})



def AddRouterDatabase(request: HttpRequest, id):
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
			try:
				MasterTarget = int(MasterTarget) if MasterTarget else None
			except ValueError:
				MasterTarget=None
			try:
				LoadTarget = LoadTarget.replace('%', '').replace(' ', '')
				if LoadTarget.isdigit():
					LoadTarget = int(LoadTarget)
				else:
					LoadTarget = None
			except AttributeError:
				LoadTarget=None
			if RouterTarget==MasterTarget:
				print("Ошибка совпадает роуетер с назначаемым мастером")
			elif not AddedRouter.objects.filter(id_application=request_app, id=MasterTarget).exists() and MasterTarget is not None:
				print("Ошибка роуетер мастер вне заявки")
				pass
			else:
				AddedRouter.objects.filter(id=RouterTarget).update(master_router_id=MasterTarget or None, router_load=LoadTarget or None)

		return redirect('application_router_url', request_app)
	
	elif request.POST.get("update_router"):
		return Response(status=status.HTTP_308_PERMANENT_REDIRECT)
		
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
			return Response("Несколько черновиков",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			AddedRouter.objects.create(id_application=ApplicationFound, id_router=Router.objects.get(id=request_id))
			return redirect('sendSearch')
			# return redirect('application_router_url', id=ApplicationFound.id)
	redirect('application_router_url')

def DeleteStatusApplicationRouterDatabase(request: HttpRequest, id):
	target = request.POST.get("application_id")
	ApplicationRouter.objects.update(date_end=datetime.now().date())
	print(target)
	with connection.cursor() as cursor:
		cursor.execute("UPDATE ApplicationRouter SET status = 'удалено' WHERE id = %s", [id])
	return redirect('sendSearch')


#REST API
#▼▼▼▼▼▼▼▼

#Домен услуги:
class StockList(APIView):
	model_class = Router
	serializer_class = RouterSerializer

@api_view(['GET'])
def GetRouter(request: Request, id, format=None):
	Router_instance = Router.objects.get(id=id)
	serializer = RouterSerializer(Router_instance)
	return Response(serializer.data)
@api_view(['GET'])
def GetFilter(request: Request, search, format=None):
	Router_list = Router.objects.filter(title__startswith=search)
	serializer = RouterSerializer(Router_list, many=True)
	return Response(serializer.data)
@api_view(['POST'])
def PostRouter(request: Request, format=None):
	serializer = RouterSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def PutRouter(request: Request, id, format=None):
	Router_list = Router.objects.get(id=id)
	serializer = RouterPUTSerializer(Router_list, data=request.data, partial=True)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def DeleteRouter(request: Request, id, format=None):
	Router_instance = Router.objects.get(id=id)
	Router_instance.delete()
	Minio_deletepicture(id)
	return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
def PostDraft(request: Request, id, format=None):

	if FindUserDraftApplication(user()):
		print("Draft найден")
		Router_instance = Router.objects.get(id=id)
		App_instance = FindUserDraftApplication(user())
		AddedRouter.objects.create(
		id_application=App_instance,
		id_router=Router_instance
		)
		serializer = AppSerializer(App_instance, data=request.data)
		pass
	else:
		Router_instance = Router.objects.get(id=id)
		
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
		pass

	# print(serializer)
	# if serializer.is_valid():
	# 	# serializer.save()
	# 	serializer.creator=user()
	# 	print(serializer)
	return Response(status=status.HTTP_201_CREATED)
@api_view(['POST'])
def PostPicture(request: Request, id, format=None):
	print("Request data:", request.data)
	print("Request FILES:", request.FILES)

	Router_instance = Router.objects.get(id=id)
	if not isinstance(request.FILES, dict):
		return Response({"Нет запроса"}, status=status.HTTP_400_BAD_REQUEST)
	else:
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
def GetIcons(request: Request, format=None):
	App_instance = ApplicationRouter.objects.filter(creator=user(), status=ApplicationRouter.Status.DRAFT).first()
	if not App_instance:
		print("ApplicationRouter вернул None")
	else:
		# serializer = RouterSerializer(App_instance)
		routers_count=AddedRouter.objects.filter(id_application=App_instance).count()
		data = {}
		data["routers_count"] = routers_count
		data["id_application"] = App_instance.pk
		return Response(data, status=status.HTTP_200_OK)
@api_view(['GET'])
def GetApps(request: Request, format=None):
	# App_instance = ApplicationRouter.objects.filter(creator=user(), status="черновик").first()
	if not isinstance(request.data, dict):
		print ("Пустой request.data")
		pass
	else:
		date_start = request.data.get("date_start")
		date_end = request.data.get("date_end")
		status_filter = request.data.get("status")
		queryset = ApplicationRouter.objects.all()
		exclude_statuses = [ApplicationRouter.Status.DELETED, ApplicationRouter.Status.DRAFT]
		queryset = queryset.exclude(status__in=exclude_statuses)
		if status_filter:
			queryset = queryset.filter(status=status_filter)
		if date_start:
			dt_start = parse_datetime(date_start)
			if dt_start:
				queryset = queryset.filter(date_create__gte=dt_start)
		if date_end:
			dt_end = parse_datetime(date_end)
			if dt_end:
				queryset = queryset.filter(date_create__lte=dt_end)
		
		# data = list(queryset.values('id', 'date_create', 'status', 'creator', 'moderator'))
		serializer = AppSerializer(queryset, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
def GetApp(request: Request, id, format=None):
	App_instance = ApplicationRouter.objects.get(id=id)
	serializer = AppAddedRouterSerializer(App_instance)
	return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['PUT'])
def PutApp(request: Request, id, format=None):
	try:
		App_instance = ApplicationRouter.objects.get(id=id)
	except ApplicationRouter.DoesNotExist:
		return Response({"Нет такой заявки."}, status=status.HTTP_404_NOT_FOUND)
	if not isinstance(request.data, dict):
		print ("Пустой request.data")
		pass
	else:
		update_data = {}
		if request.data.get("Adress"):
			update_data["Adress"] = request.data.get("Adress")
		if request.data.get("TotalUsers"):
			update_data["TotalUsers"] = request.data.get("TotalUsers")
		serializer = AppSerializer(App_instance, data=update_data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def PutComplete(request: Request, id, format=None):
	try:
		App_instance = ApplicationRouter.objects.get(id=id)
	except ApplicationRouter.DoesNotExist:
		return Response({"Нет такой заявки."}, status=status.HTTP_404_NOT_FOUND)
	
	if App_instance.TotalUsers is None:
		return Response({"Нет нужных полей."}, status=status.HTTP_400_BAD_REQUEST)
	
	if App_instance.status==ApplicationRouter.Status.FORMULATED or App_instance.status==ApplicationRouter.Status.REJECTED:
		return Response({"Нет прав."}, status=status.HTTP_403_FORBIDDEN)
	
	update_data = {}
	update_data["status"] = ApplicationRouter.Status.FORMULATED
	update_data["date_modific"] = datetime.now().date()
	serializer = AppSerializer(App_instance, data=update_data, partial=True)
	if serializer.is_valid():
		serializer.save()
		return Response(status=status.HTTP_201_CREATED)
	return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def PutModerator(request: Request, id, format=None):
	try:
		App_instance = ApplicationRouter.objects.get(id=id)
	except ApplicationRouter.DoesNotExist:
		return Response({"Нет такой заявки."}, status=status.HTTP_404_NOT_FOUND)
	
	if not App_instance.status==ApplicationRouter.Status.FORMULATED:
		return Response({"Нет прав."}, status=status.HTTP_403_FORBIDDEN)
	
	if not isinstance(request.data, dict):
		print ("Пустой request.data")
		pass
	else:
		update_data = {}
		if request.data.get("status" ) == ApplicationRouter.Status.COMPLETED:
			update_data["status"] = ApplicationRouter.Status.COMPLETED
			update_data["date_end"] = datetime.now().date()
			update_data["moderator"] = user()
			serializer = AppSerializer(App_instance, data=update_data, partial=True)
			if serializer.is_valid():
				serializer.save()
				Router_list = AddedRouter.objects.filter(id_application=App_instance)
				SumLoadCheck: int = 0
				for RouterSelect in Router_list:
					if RouterSelect.router_load is not None:
						SumLoadCheck+=RouterSelect.router_load
				for RouterSelect in Router_list:
					if RouterSelect.router_load is None or RouterSelect.router_load == '':
						RouterSelect.router_load=CalculateLoad(Router_list.count(), SumLoadCheck)
						RouterSelect.save()
				return Response(status=status.HTTP_201_CREATED)
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		elif request.data.get("status" ) == ApplicationRouter.Status.REJECTED:
			update_data["status"] = ApplicationRouter.Status.REJECTED
			update_data["date_end"] = datetime.now().date()
			update_data["moderator"] = user()
			serializer = AppSerializer(App_instance, data=update_data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(status=status.HTTP_201_CREATED)
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def DeleteApp(request: Request, id, format=None):
	try:
		App_instance = ApplicationRouter.objects.get(id=id)
	except ApplicationRouter.DoesNotExist:
		return Response({"Нет такой заявки."}, status=status.HTTP_404_NOT_FOUND)
	if App_instance.status==ApplicationRouter.Status.FORMULATED or App_instance.status==ApplicationRouter.Status.REJECTED:
		return Response({"Нет прав."}, status=status.HTTP_403_FORBIDDEN)
	update_data = {}
	update_data["status"] = ApplicationRouter.Status.DELETED
	update_data["date_modific"] = datetime.now().date()
	serializer = AppSerializer(App_instance, data=update_data, partial=True)
	if serializer.is_valid():
		serializer.save()
		return Response(status=status.HTTP_204_NO_CONTENT)
	return Response(status=status.HTTP_400_BAD_REQUEST)

#Домен м-м:
@api_view(['DELETE'])
def DeleteAdded(request: Request, id, format=None):
	try:
		App_instance = FindUserDraftApplication(user())
	except:
		return Response({"Нет черновой завки"},status=status.HTTP_404_NOT_FOUND)
	try:
		Router_instance = AddedRouter.objects.get(id_router=id, id_application=App_instance)
	except MultipleObjectsReturned:
		Router_instance = AddedRouter.objects.filter(id_router=id, id_application=App_instance).last()
		if Router_instance:
			Router_instance.delete()
		else:
			return Response({"куда то пропал роутер"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	except ObjectDoesNotExist:
		return Response({"Нет такого роутера"},status=status.HTTP_404_NOT_FOUND)
	else:
		Router_instance.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['PUT'])
def PutAdded(request: Request, id, format=None):
	App_instance = FindUserDraftApplication(user())
	if not App_instance:
		return Response({"error": "AddedRouter не найден"}, status=status.HTTP_404_NOT_FOUND)
	Router_instance = AddedRouter.objects.filter(id_router=id, id_application=App_instance).last()
	if not Router_instance:
		return Response({"error": "ApplicationRouter не найден"}, status=status.HTTP_404_NOT_FOUND)
	serializer = AddedSerializer(Router_instance, data=request.data, partial=True)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

#Домен пользователь:
@api_view(['POST'])
@permission_classes([AllowAny])
def PostRegister(request: Request, format=None):
	serializer = UserRegisterSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(status=status.HTTP_201_CREATED)
	return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUser(request: Request, id, format=None):
	if request.user.id != id and not request.user.is_staff:
		return Response({"Доступ запрещён."}, status=status.HTTP_403_FORBIDDEN)
	try:
		user = User.objects.get(id=id)
	except User.DoesNotExist:
		return Response({"Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)
	serializer = UserDetailSerializer(user)
	return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def PutUser(request: Request, format=None):
	user = request.user
	serializer = UserDetailSerializer(user, data=request.data, partial=True)
	if serializer.is_valid():
		serializer.save()
		return Response(status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def PostAuth(request: Request, format=None):
	if not isinstance(request.data, dict):
		return Response({"detail": "Заполните имя пользователя и пароль."}, status=status.HTTP_400_BAD_REQUEST)
	else:
		user_request=request.data.get("username")
		password_request=request.data.get("password")
		user = authenticate(request._request, username=user_request, password=password_request)
		if user is not None:
			login(request._request, user)
			token, created = Token.objects.get_or_create(user=user)
			return Response({"token": token.key, "user": UserDetailSerializer(user).data},status=status.HTTP_200_OK)
	return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def PostExit(request: Request, format=None):
	if request.user.is_authenticated:
		Token.objects.filter(user=request.user).delete()
		logout(request._request)
		return Response(status=status.HTTP_200_OK)
	else:
		return Response({"Вы уже не авторизованы."}, status=status.HTTP_400_BAD_REQUEST)


def user():
	try:
		user1 = User.objects.get(id=1)
	except:
		pass
	return user1

def FindUserDraftApplication(UserFind):
	result=ApplicationRouter.objects.filter(creator=UserFind, status=ApplicationRouter.Status.DRAFT).first()
	if result:
		FoundApplication: ApplicationRouter = result 
	else:
		print('Ничего не найдено')
		pass
	return FoundApplication

def CalculateLoad(number_of_routers: int, already_used_load: float = 0):
	if already_used_load>=100:
		return 0
	result=(100-already_used_load)/number_of_routers
	result=int(result)
	return result