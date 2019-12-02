from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('news/', views.news, name = 'newsPage'),
    path('accounts/confirming_registration', views.confirming_register, name='reg_confirm'),
    path('accounts/register/', views.register, name='register'),
    path('news/submit_request', views.requests_handle, name='submit_request'),
    path('test/', views.test, name='test'),
    path('feedback/', views.feedback, name='feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)