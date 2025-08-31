from django.shortcuts import render, redirect
from .forms import EmailForm
from .models import Email
from .nlp_utils import triagem_email, gerar_resposta
from django.core.paginator import Paginator
import PyPDF2

# formulário para usuário comum
def email_upload(request):
    form = EmailForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        email = form.save(commit=False)
        # Se o arquivo foi enviado, leia o conteúdo
        if email.arquivo:
            ext = email.arquivo.name.split('.')[-1].lower()
            if ext == 'txt':
                email.texto = email.arquivo.read().decode('utf-8')
            elif ext == 'pdf':
                pdf = PyPDF2.PdfReader(email.arquivo)
                texto_pdf = ""
                for page in pdf.pages:
                    texto_pdf += page.extract_text()
                email.texto = texto_pdf
        email.produtivo = triagem_email(email.texto)
        email.resposta = gerar_resposta(email.produtivo)
        email.save()
        return redirect('classificacao:email_upload')
    return render(request, 'email_upload.html', {'form': form})

# formulário para admin
def email_upload_admin(request):
    form = EmailForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        email = form.save(commit=False)
        # Se o arquivo foi enviado, leia o conteúdo
        if email.arquivo:
            ext = email.arquivo.name.split('.')[-1].lower()
            if ext == 'txt':
                email.texto = email.arquivo.read().decode('utf-8')
            elif ext == 'pdf':
                pdf = PyPDF2.PdfReader(email.arquivo)
                texto_pdf = ""
                for page in pdf.pages:
                    texto_pdf += page.extract_text()
                email.texto = texto_pdf
        email.produtivo = triagem_email(email.texto)
        email.resposta = gerar_resposta(email.produtivo)
        email.save()
        return redirect('email_list')
    return render(request, 'email_upload.html', {'form': form})

# listagem de emails
def email_list(request):
    emails = Email.objects.all().order_by('-received_at')
    
    # Estatísticas
    total_emails = emails.count()
    emails_produtivos = emails.filter(produtivo=True).count()
    emails_improdutivos = total_emails - emails_produtivos
    
    # Paginação
    paginator = Paginator(emails, 10)  # 10 emails por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_emails': total_emails,
        'emails_produtivos': emails_produtivos,
        'emails_improdutivos': emails_improdutivos,
    }
    return render(request, 'email_list.html', context)