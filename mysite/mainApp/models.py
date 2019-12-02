from django.db import models
from django.utils import timezone
# Create your models here.


class News(models.Model):
	title = models.TextField(null=True)
	text = models.TextField(null = True)
	pub_date = models.DateTimeField(default=timezone.now)
	tag = models.TextField(default="Другое")
	amount_of_views = models.IntegerField(default=0)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'News'


class Course(models.Model):
	name = models.TextField(max_length=30)

	def __str__(self):
		return self.name


class RequestRegistration(models.Model):
	name = models.TextField(max_length=100)
	contact_number = models.TextField(max_length=15)
	service_type = models.ForeignKey(Course, on_delete=models.CASCADE)

class Task(models.Model):
	EASY = '1. Легкий'
	MEDIUM = '2. Средний'
	HARD = '3. Сложный'
	DIFFICULTY = [
		(EASY, 'Легкий'),
		(MEDIUM, 'Средний'),
		(HARD, 'Сложный'),
	]

	topic = models.CharField('Название темы', max_length=200)
	difficulty = models.CharField(max_length=50, choices=DIFFICULTY, default=EASY)
	s_description = models.CharField('Наименование задачи', max_length=200)
	f_description = models.TextField('Описание задачи', max_length=1000, default="Fully")

	def __str__(self):
		return self.topic

