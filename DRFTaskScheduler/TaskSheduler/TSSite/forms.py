from datetime import datetime
import re

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from TSApi.models import TaskElectricalModel
from TSApi import utils


        
        
class TaskForm(forms.ModelForm):
    city = forms.CharField(max_length=250, initial="Сегежа", label="город")
    apartment = forms.CharField(max_length=10, required=False, label="квартира")
    note = forms.CharField(widget=forms.Textarea(attrs={"class": "input-text"}), label="примечания",required=False)
    date_deadline = forms.CharField(max_length=10, required=False, label="на какое число")
    class Meta:
        model = TaskElectricalModel
        fields = ["date_registration", "date_deadline", "city", "street", "house", "apartment", "task", "note"]
        widgets = {
            "task": forms.Textarea(attrs={"class": "input-text"}),
            "note": forms.Textarea(attrs={"class": "input-text"}),
        }
    
    def clean_street(self):
        street = self.cleaned_data["street"].title()
        return street
    
    def clean_date_registration(self):
        date = self.cleaned_data["date_registration"]
        if not date:
            dt = datetime.today()
            dt = dt.strftime('%d.%m.%Y')
            return dt
        pattern = r"\d\d\.\d\d\.\d\d\d\d"
        if not re.fullmatch(pattern, date):
            raise ValidationError("Дата должна быть формата: дд.мм.гггг")
        d, m, y = map(int, date.split('.'))
        dt = datetime(y, m, d)
        cd = datetime.today()
        if dt > cd:
            raise ValidationError("Данная дата еще не наступила")
        return date


class TaskUpdateForm(forms.ModelForm):

    city = forms.CharField(max_length=250, initial="Сегежа", label="город")
    apartment = forms.CharField(max_length=10, required=False, label="квартира")
    date_deadline = forms.CharField(max_length=10, required=False, label="на какое число")
    note = forms.CharField(widget=forms.Textarea(attrs={"class": "input-text"}), label="примечания",required=False)
    class Meta:
        model = TaskElectricalModel
        fields = ["date_registration", "date_deadline", "city", "street", "house", "apartment", "task", "note"]
        widgets = {
            "task": forms.Textarea(attrs={"class": "input-text"}),
            "note": forms.Textarea(attrs={"class": "input-text"}),
        }
    
    def clean_street(self):
        street = self.cleaned_data["street"].title()
        return street


class WorkUpdateForm(forms.ModelForm):
    date_execution = forms.CharField(max_length=10, label="дата выполнения")
    complited_work = forms.CharField(label="выполненые работы", widget=forms.Textarea(attrs={"class":"input-text", "cols": "70", "rows":"10"})),
    class Meta:
        model = TaskElectricalModel
        fields = ("date_execution", "complited_work", "materials_used", "payment_amount", "note")
        widgets = {
            "materials_used": forms.Textarea(attrs={"class":"input-text"}),
            "note": forms.Textarea(attrs={"class":"input-text"}),
        }

    def clean_date_execution(self):
        date = self.cleaned_data["date_execution"]
        if not date:
            dt = datetime.today()
            dt = dt.strftime('%d.%m.%Y')
            return dt
        pattern = r"\d\d\.\d\d\.\d\d\d\d"
        if not re.fullmatch(pattern, date):
            raise ValidationError("Дата должна быть формата: дд.мм.гггг")
        d, m, y = map(int, date.split('.'))
        dt = datetime(y, m, d)
        cd = datetime.today()
        if dt > cd:
            raise ValidationError("Данная дата еще не наступила")
        return date


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=30, label="Имя пользователя: ", widget=forms.TextInput(attrs={'class': 'lg-input'}))
    password = forms.CharField(max_length=30, label="Пароль: ", widget=forms.PasswordInput(attrs={'class': 'lg-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
    

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=30, label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'rg-input'}))
    password1 = forms.CharField(max_length=30, label="Введите пароль", min_length=5, widget=forms.PasswordInput(attrs={'class': 'rg-input'}))
    password2 = forms.CharField(max_length=30, label="Повторите пароль", min_length=5, widget=forms.PasswordInput(attrs={'class': 'rg-input'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username or len(username) < 4:
            raise ValidationError("Имя должно быть не менее 4 символов")
        return username

    def clean_password1(self) -> str:
        password = self.cleaned_data['password1']
        alpha = filter(str.isalpha, password)
        digits = filter(str.isdigit, password)
        if not alpha or not digits:
            raise ValidationError(('пароль должен состоять из чисел и букв'))
        return password

    def clean_password2(self) -> str:
        return super().clean_password2()








