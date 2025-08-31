from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'classificacao_admin'

urlpatterns = [
    path('upload/', login_required(views.email_upload_admin), name='email_upload_admin'),
    path('lista/', login_required(views.email_list), name='admin_email_list'),
]