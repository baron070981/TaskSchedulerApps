from django.db import models
from django.urls import reverse
import datetime

from . import utils






class TaskElectricalModel(models.Model):

    # dd.mm.yyyy

    date_creation = models.CharField(max_length=10, verbose_name="дата создания", default=utils.get_date_str()) # дата создания записи. 
    date_registration = models.CharField(max_length=10, verbose_name="дата заявки", default=utils.get_date_str()) # дата получения заявки. По умолчанию совпадает с датой создания
    date_execution = models.CharField(max_length=10, verbose_name="дата выполнения", blank=True) # дата выполнения заявки. Если поле пустое - заявка не выполнена
    date_deadline = models.CharField(max_length=10, verbose_name="на какое число", blank=True) # дата когда должна быть выполнена заявка

    city = models.CharField(max_length=250, default="Сегежа", verbose_name="город") # город +
    street = models.CharField(max_length=250, verbose_name="улица") # улица +
    house = models.CharField(max_length=10, verbose_name="номер дома") # номер дома. Может быть: 12/2 или 12 к. 2 или 12Б +
    apartment = models.CharField(max_length=10, verbose_name="квартира", blank=True) # номер квартры. Может быть: 1 или 1А -

    task = models.TextField(verbose_name="заявка") # заявка +
    complited_work = models.TextField(verbose_name="выполенные работы", blank=True) # выполненные работы, если заявка выполнена -
    materials_used = models.TextField(verbose_name="материалы", blank=True) # использованные материалы -
    payment_amount = models.FloatField(verbose_name="сумма оплаты", default=0.0) # сумма оплаты, если заявка была платной -
    note = models.TextField(verbose_name="примечания", blank=True) # примечания -

    class Meta:
        verbose_name = 'Заявка на работу'
        verbose_name_plural = 'Заявки на работы'
        ordering = ['-pk']
        app_label = "TSApi"


    def __str__(self):
        return f"{self.date_registration} {self.city} {self.street} {self.house}"


    def get_absolute_url(self):
        return reverse("detail_task", kwargs={"task_id": self.pk})
    


if __name__ == "__main__":
    ...









