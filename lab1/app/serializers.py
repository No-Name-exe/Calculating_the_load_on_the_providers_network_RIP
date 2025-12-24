from .models import Router, ApplicationRouter, AddedRouter
from django.contrib.auth.models import User
from rest_framework import serializers

class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = User
		# Поля, которые мы сериализуем
		fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserRegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'password']
	
	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		return user

class RouterSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = Router
		# Поля, которые мы сериализуем
		fields = ["id", "title", "desc", "img", "status"]

class RouterPUTSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = Router
		# Поля, которые мы сериализуем
		fields = ["title", "desc", "img"]

class AddedSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = AddedRouter
		# Поля, которые мы сериализуем
		fields = ["id_application", "id_router", "master_router_id", "router_load"]

class AddedPUTSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = AddedRouter
		# Поля, которые мы сериализуем
		fields = ["master_router_id", "router_load"]

class AppSerializer(serializers.ModelSerializer):
	# вложенный сериализатор
	creator = serializers.SlugRelatedField(read_only=True, slug_field='username')
	moderator = serializers.SlugRelatedField(read_only=True, slug_field='username')

	class Meta:
		# Модель, которую мы сериализуем
		model = ApplicationRouter

		# Поля, которые мы сериализуем
		fields = ["id", "creator", "moderator", "status", "date_create", "date_modific", "date_end", "Adress", "TotalUsers"]

class AppPUTSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = ApplicationRouter

		# Поля, которые мы сериализуем
		fields = ["Adress", "TotalUsers"]

class AppAddedRouterSerializer(serializers.ModelSerializer):
	# вложенный сериализатор
	creator = serializers.SlugRelatedField(read_only=True, slug_field='username')
	moderator = serializers.SlugRelatedField(read_only=True, slug_field='username')
	ListRouter = serializers.SerializerMethodField()

	class Meta:
		# Модель, которую мы сериализуем
		model = ApplicationRouter

		# Поля, которые мы сериализуем
		fields = ["id", "creator", "moderator", "status", "date_create", "date_modific", "date_end", "Adress", "TotalUsers", "ListRouter"]

	def get_ListRouter(self, obj):
		# Получаем все объекты AddedRouter, связанные с текущей заявкой
		added_relations = AddedRouter.objects.filter(id_application=obj)
		# Сериализуем их с помощью вашего сериализатора AddedSerializer
		return AddedForAppSerializer(added_relations, many=True).data

class AddedForAppSerializer(serializers.ModelSerializer):
	Router = serializers.SerializerMethodField()
	class Meta:
		# Модель, которую мы сериализуем
		model = AddedRouter
		# Поля, которые мы сериализуем
		fields = ["id", "id_router", "master_router_id", "router_load", "Router"]

	def get_Router(self, obj):
		# Получаем все объекты AddedRouter, связанные с текущей заявкой
		router_relations = Router.objects.filter(id=obj.id_router.id)
		# Сериализуем их с помощью вашего сериализатора AddedSerializer
		return RouterPUTSerializer(router_relations, many=True).data
	

class UserTokenSerializer(serializers.ModelSerializer):
	token = serializers.CharField()
	user = UserDetailSerializer()
	class Meta:
		model = User
		fields = ['token', 'user']

class UserAuthSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = User
		# Поля, которые мы сериализуем
		fields = ['username', 'password']