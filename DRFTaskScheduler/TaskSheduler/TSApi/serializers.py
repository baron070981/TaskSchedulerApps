from __future__ import annotations
from django.contrib.auth.models import User, Group
from rest_framework import serializers
import re
from dataclasses import dataclass

from . models import *
from . utils import *



class TasksSerializer(serializers.ModelSerializer):
    date_creation = serializers.CharField(max_length=10, read_only=True, default=get_date_str())
    city = serializers.CharField(max_length=250, default="Сегежа")
    class Meta:
        model = TaskElectricalModel
        fields = "__all__"
        # exclude = ["date_creation"]


class TasksUpdateSerializer(serializers.ModelSerializer):
    date_creation = serializers.CharField(max_length=10, read_only=True, default=get_date_str())
    city = serializers.CharField(max_length=250, default="Сегежа", allow_blank=True)

    class Meta:
        model = TaskElectricalModel
        fields = "__all__"
    
    def update(self, instance, validated_data):
        instance.date_creation = instance.date_creation
        instance.date_registration = instance.date_registration
        instance.date_execution = validated_data.get("date_execution", instance.date_execution)
        instance.city = validated_data.get("city", instance.city)
        instance.street = validated_data.get("street", instance.street)
        instance.house = validated_data.get("house", instance.house)
        instance.apartment = validated_data.get("apartment", instance.apartment)
        instance.task = validated_data.get("task", instance.task)
        instance.complited_work = instance.complited_work
        instance.materials_used = instance.materials_used
        instance.payment_amount = instance.payment_amount
        instance.note = validated_data.get("note", instance.note)
        instance.save()
        return instance


class TasksWorkUpdateSerializer(serializers.ModelSerializer):
    date_creation = serializers.CharField(max_length=10, read_only=True, default=get_date_str())
    city = serializers.CharField(max_length=250, default="Сегежа")
    date_execution = serializers.CharField(max_length=10)

    class Meta:
        model = TaskElectricalModel
        fields = "__all__"
    
    def update(self, instance, validated_data):
        instance.date_creation = instance.date_creation
        instance.date_registration = instance.date_registration
        instance.date_execution = validated_data.get("date_execution", instance.date_execution)
        instance.city = instance.city
        instance.street = instance.street
        instance.house = instance.house
        instance.apartment = instance.apartment
        instance.task = instance.task
        instance.complited_work = validated_data.get("complited_work", instance.complited_work)
        instance.materials_used = validated_data.get("materials_used", instance.materials_used)
        instance.payment_amount = validated_data.get("payment_amount", instance.payment_amount)
        instance.note = validated_data.get("note", instance.note)
        instance.save()
        return instance


class TasksUpdateSerializer_(serializers.Serializer):

    # date_creation
    # date_registration
    # date_execution
    # city
    # street
    # house
    # apartment
    # task
    # complited_work 
    # materials_used
    # payment_amount
    # note

    date_creation = serializers.CharField(max_length=10, read_only=True, default=get_date_str()) # дата создания записи. 
    date_registration = serializers.CharField(max_length=10, default=get_date_str(), allow_blank=True) # дата получения заявки. По умолчанию совпадает с датой создания
    date_execution = serializers.CharField(max_length=10, allow_blank=True, required=True) # дата выполнения заявки. Если поле пустое - заявка не выполнена

    city = serializers.CharField(max_length=250, default="Сегежа") # город +
    street = serializers.CharField(max_length=250) # улица +
    house = serializers.CharField(max_length=10) # номер дома. Может быть: 12/2 или 12 к. 2 или 12Б +
    apartment = serializers.CharField(max_length=10, allow_blank=True) # номер квартры. Может быть: 1 или 1А -

    task = serializers.CharField() # заявка +
    complited_work = serializers.CharField(allow_blank=True) # выполненные работы, если заявка выполнена -
    materials_used = serializers.CharField(allow_blank=True) # использованные материалы -
    payment_amount = serializers.FloatField(default=0.0) # сумма оплаты, если заявка была платной -
    note = serializers.CharField(allow_blank=True) # примечания -



















