from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	username = forms.CharField(required=True)
	password1 = forms.PasswordInput()
	password2 = forms.PasswordInput()

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
# Конструктор данного класса я использовал только для того чтобы очистить поля help_text которые заполняются по
# - умолчанию из коробки Django

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)

# Очищение help_text во всех полях которых я использую
		for field_name in ['username', 'password1', 'password2']:
			self.fields[field_name].help_text = None

# Переопределение содержимых label которые отображаются в HTML формах на свои
		self.fields['password1'].label = 'Пароль'
		self.fields['password2'].label = 'Подтверждение пароля'
		self.fields['username'].label = 'Имя пользователя'
		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'
		self.fields['email'].label = 'Электронная почта'

# Данный метод определяет за регистрацию нового пользователя в базе данных
	def save(self, commit=True):
		user = super(CustomRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.set_password(self.cleaned_data['password1'])
		user.is_active = False

		if commit:
			user.save()

		return user