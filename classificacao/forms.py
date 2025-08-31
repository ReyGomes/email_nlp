from django import forms
from .models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['assunto', 'texto', 'arquivo']
        labels = {
            'assunto': 'Assunto do e-mail',
            'texto': 'Mensagem',
            'arquivo': 'Arquivo (.txt ou .pdf)'
        }
        widgets = {
            'assunto': forms.TextInput(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }