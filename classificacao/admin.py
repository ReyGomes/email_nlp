from django.contrib import admin
from .models import Email

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['id', 'assunto', 'produtivo', 'received_at']
    list_filter = ['produtivo', 'received_at']
    search_fields = ['assunto', 'texto', 'resposta']
    readonly_fields = ['received_at']
    
    # Fieldsets com os campos corretos
    fieldsets = [
        ('Informações Básicas', {
            'fields': ['assunto', 'produtivo', 'received_at']
        }),
        ('Conteúdo', {
            'fields': ['texto', 'resposta', 'arquivo'],
            'classes': ['wide']
        }),
    ]