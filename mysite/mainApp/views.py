from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template.context_processors import csrf
from django.urls import reverse
from django.core.mail import send_mail
from .models import *
from random import randint
from .forms import CustomRegistrationForm
from django.utils import timezone
import operator

def index(request):
    courses = Course.objects.all()
    context = {'courses' : courses}
    return render(request, 'mainApp/index.html', context)

def feedback(request):
    courses = Course.objects.all()
    context = {'courses' : courses}
    return render(request, 'mainApp/feedback.html', context)

def test(request):
    topics = Task.objects.order_by('topic')
    names = set()
    for name in topics:
        names.add(name.topic)
    names = sorted(names)
    tasks = Task.objects.all()
    print(tasks)
    if request.method == 'POST':
        topic_name = request.POST['Темы']
        if topic_name == 'Все':
            context = {'topics' : names, 'tasks': tasks}
            return render(request, 'mainApp/inside.html', context)
        tasks = Task.objects.filter(topic= topic_name)
    tasks = sorted(tasks, key=operator.attrgetter('difficulty', 'topic'))
    for task in tasks:
        task.difficulty = task.difficulty[2:]
    context = {'topics' : names, 'tasks': tasks}
    return render(request, 'mainApp/inside.html', context)

def news(request):
    news = News.objects.all()[:4]
    courses = Course.objects.all()
    context = {'news': news, 'courses': courses}
    return render(request, 'mainApp/newsPage.html', context)


def register(request):
    courses = Course.objects.all()
    context = {'courses' : courses}
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            secret_code = randint(1000, 9999)
            header_of_the_message = 'Подтверждение с почты'
            content = """
			your secret code is {}	
			""".format(secret_code)
            send_mail(header_of_the_message, content, "AByera's website",
                      recipient_list=[form.cleaned_data['email']]
                      , fail_silently=False)
            request.session.update({'form': {'username': form.cleaned_data['username'],
                                             'secret_code': secret_code}})
            # form.save()
            return HttpResponseRedirect('/accounts/confirming_registration')
        else:
            return render_to_response('mainApp/register.html', {'form': form})
    args = {}
    args.update(csrf(request))
    args['form'] = CustomRegistrationForm()
    return render_to_response('mainApp/register.html', args, context)


def confirming_register(request):
    courses = Course.objects.all()
    context = {'courses' : courses}
    session = request.session
    if request.method == 'POST':
        if session['form']['secret_code'] == int(request.POST['code_by_user']):
            username = session['form']['username']
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/accounts/login',)
        else:
            return render(request, 'mainApp/confirm.html',
                          {'result': 'Секретный код был введен неверно! Регистрация отменена!'})
    return render(request, 'mainApp/confirm.html', {})


def requests_handle(request):
    try:
        if request.method == 'POST':
            name = str(request.POST['Имя'])
            phone_number = str(request.POST['Телефон'])
            course_from_client = str(request.POST['Услуга'])
            course = Course.objects.get(name=course_from_client)
            RequestRegistration.objects.create(name=name, contact_number=phone_number, service_type=course)
            send_mail(subject='Заявка от {}'.format(name)
                      , message='{} оставил заявку на курс {}!\nНомер телефона: {}\nДата заявки: {}'.format(name, course.name, phone_number, timezone.now()),
					  from_email='Заявка на курс!',
                      recipient_list=['A.Amirov2000@gmail.com','bakubayevio@gmail.com']
                      , fail_silently=False)
        return HttpResponseRedirect(reverse('index'))
    except:
        raise Http404("Запрашиваемая страница не найдена")
