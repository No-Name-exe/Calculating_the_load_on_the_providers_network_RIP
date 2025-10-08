from .models import Router, ApplicationRouter, AddedRouter
from django.contrib.auth.models import User
from rest_framework import serializers

class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = User
		# Поля, которые мы сериализуем
		fields = ['id', 'username', 'first_name', 'last_name', 'email']

class RouterSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = Router
		# Поля, которые мы сериализуем
		fields = ["id", "title", "desc", "img", "status"]

class AddedSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = AddedRouter
		# Поля, которые мы сериализуем
		fields = ["id_application", "id_router", "master_router_id", "router_load"]

class AppSerializer(serializers.ModelSerializer):
	class Meta:
		# Модель, которую мы сериализуем
		model = ApplicationRouter
		# вложенный сериализатор
		creator = UserDetailSerializer(read_only=True)
		moderator = UserDetailSerializer(read_only=True)
		# Поля, которые мы сериализуем
		fields = ["id", "creator", "moderator", "status", "date_create", "date_modific", "date_end", "Adress", "TotalUsers"]
