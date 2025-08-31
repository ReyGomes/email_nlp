from django.urls import path
from . import views

app_name = 'classificacao'

urlpatterns = [
    path('upload/', views.email_upload, name='email_upload'),
    # path('emails/', views.lista_emails, name='emails'),  # listagem pós MLP
]