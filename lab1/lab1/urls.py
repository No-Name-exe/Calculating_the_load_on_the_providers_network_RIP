"""
URL configuration for lab1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from app import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
		title="Router Load API",
		default_version='v1',
		description="Документация API",
		terms_of_service="https://www.google.com/policies/terms/",
		contact=openapi.Contact(email="contact@snippets.local"),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', views.GetRouters, name='sendSearch'),
	path('router/<int:id>/', views.GetRouterHttp, name='router_url'),
	path('application/<int:id>/', views.GetApplicationRouter, name='application_router_url'),
	path('addrouter/<int:id>/', views.AddRouterDatabase, name='router_add'),
	path('application_router_delete/<int:id>', views.DeleteStatusApplicationRouterDatabase, name='application_router_delete'),

	path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

	# path('accounts/login/',  views.PostAuth, name='login'),
	# path('accounts/logout/', views.PostExit, name='logout'),
	
	# REST API
	# """  
	# Домен услуги:
	# GET список с фильтрацией
	# GET одна запись
	# POST добавление (без изображения)
	# PUT изменение
	# DELETE удаление. Удаление изображения встроено в метод удаления услуги
	# POST добавления в заявку-черновик. Заявка создается пустой, указывается автоматически создатель, дата создания и статус, остальные поля указываются через PUT или смену статуса
	# POST добавление изображения. Добавление изображения по id услуги, старое изображение заменяется/удаляется. minio только в этом методе и удалении! Название изображение генерируется на латинице
	# 
	# Домен заявки:
	# GET иконки корзины (без входных параметров, ид заявки вычисляется). Возвращается id заявки-черновика этого пользователя и количество услуг в этой заявке
	# GET список (кроме удаленных и черновика, поля модератора и создателя через логины) с фильтрацией по диапазону даты формирования и статусу
	# GET одна запись (поля заявки + ее услуги). При получении заявки возвращется список ее услуг с картинками
	# PUT изменения полей заявки по теме
	# PUT сформировать создателем (дата формирования). Происходит проверка на обязательные поля
	# PUT завершить/отклонить модератором. При завершить/отклонении заявки проставляется модератор и дата завершения. Одно из доп. полей заявки или м-м рассчитывается (реализовать формулу представленную в лаб-2) при завершении заявки (вычисление стоимости заказа, даты доставки в течении месяца, вычисления в м-м).
	# DELETE удаление (дата формирования)
	# 
	# Домен м-м:
	# DELETE удаление из заявки (без PK м-м)
	# PUT изменение количества/порядка/значения в м-м (без PK м-м)
	# 
	# Домен пользователь:
	# POST регистрация
	# GET полей пользователя после аутентификации (для личного кабинета)
	# PUT пользователя (личный кабинет)
	# POST аутентификация
	# POST деавторизация 
	# """
	path('api/', include([
		path('Routers/', include([
			path('<int:id>/', views.GetRouter, name='api_Routers_get_url'),# GET одна запись
			re_path(r'^filter/(?P<search>.*)/$', views.GetFilter, name='api_Routers_filter_url'),# GET список с фильтрацией
			path('add/', views.PostRouter, name='api_Routers_add_url'),# POST добавление (без изображения)
			path('put/<int:id>/', views.PutRouter, name='api_Routers_put_url'),# PUT изменение
			path('delete/<int:id>/', views.DeleteRouter, name='api_Routers_delete_url'),# DELETE удаление. Удаление изображения встроено в метод удаления услуги
			path('draft/<int:id>/', views.PostDraft, name='api_Routers_draft'),# POST добавления в заявку-черновик. Заявка создается пустой, указывается автоматически создатель, дата создания и статус, остальные поля указываются через PUT или смену статуса
			path('addpicture/<int:id>/', views.PostPicture, name='api_Routers_addpicture_url'),# POST добавление изображения. Добавление изображения по id услуги, старое изображение заменяется/удаляется. minio только в этом методе и удалении! Название изображение генерируется на латинице
		])),
		path('AppRouters/', include([
			path('icon/', views.GetIcons, name='api_AppRouters_icons_url'),# GET иконки корзины (без входных параметров, ид заявки вычисляется). Возвращается id заявки-черновика этого пользователя и количество услуг в этой заявке
			path('filter/', views.GetApps, name='api_AppRouters_list_url'),# GET список (кроме удаленных и черновика, поля модератора и создателя через логины) с фильтрацией по диапазону даты формирования и статусу
			path('<int:id>/', views.GetApp, name='api_AppRouters_get_url'),# GET одна запись (поля заявки + ее услуги). При получении заявки возвращется список ее услуг с картинками
			path('put/<int:id>/', views.PutApp, name='api_AppRouters_put_url'),# PUT изменения полей заявки по теме
			path('complete/<int:id>/', views.PutComplete, name='api_AppRouters_complete_url'),# PUT сформировать создателем (дата формирования). Происходит проверка на обязательные поля
			path('mod/<int:id>/', views.PutModerator, name='api_AppRouters_moderator_url'),# PUT завершить/отклонить модератором. При завершить/отклонении заявки проставляется модератор и дата завершения. Одно из доп. полей заявки или м-м рассчитывается (реализовать формулу представленную в лаб-2) при завершении заявки (вычисление стоимости заказа, даты доставки в течении месяца, вычисления в м-м).
			path('delete/<int:id>/', views.DeleteApp, name='api_AppRouters_delete_url'),# DELETE удаление (дата формирования)
		])),
		path('AddedRouters/', include([
			path('delete/<int:id>/', views.DeleteAdded, name='api_AddedRouters_delete_url'),# DELETE удаление из заявки (без PK м-м)
			path('change/<int:id>/', views.PutAdded, name='api_AddedRouters_put_url'),# PUT изменение количества/порядка/значения в м-м (без PK м-м)
		])),
		path('User/', include([
			path('register/', views.PostRegister, name='api_User_register_url'),# POST регистрация
			path('<int:id>/', views.GetUser, name='api_User_get_url'),# GET полей пользователя после аутентификации (для личного кабинета)
			path('account/', views.PutUser, name='api_User_put_url'),# PUT пользователя (личный кабинет)
			path('auth/', views.PostAuth, name='api_User_auth_url'),# POST аутентификация
			path('exit/', views.PostExit, name='api_User_exit_url'),# POST деавторизация
		])),
	])),


]
