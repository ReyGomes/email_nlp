# classificacao/nlp_utils.py
from transformers import pipeline
from django.conf import settings

classifier = pipeline(
    "text-classification",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    token=settings.HUGGINGFACE_TOKEN if hasattr(settings, 'HUGGINGFACE_TOKEN') else None
)

# Lista REVISADA de palavras-chave (menos agressiva)
palavras_improdutivas = [
    'promoção', 'oferta exclusiva', 'spam', 'propaganda',
    'desconto imperdível', 'grátis', 'ganhe', 'compre agora',
    'oferta limitada', 'black friday', 'cyber monday',
    'gratuito', 'aproveite já', 'liquidação'
]

def triagem_email(texto):
    texto_lower = texto.lower()
    
    # 1. Filtragem por palavras-chave - apenas palavras MUITO específicas
    for palavra in palavras_improdutivas:
        if palavra in texto_lower:
            print(f"🚫 Bloqueado por palavra-chave: {palavra}")
            return False  # improdutivo

    # 2. Classificação pelo modelo
    try:
        result = classifier(texto)
        label = result[0]['label']
        score = result[0]['score']
        print(f"📊 Modelo NLP: {label} (score: {score:.3f})")
        
        # Modelo retorna '1 star', '2 stars', ..., '5 stars'
        if '5' in label or '4' in label:
            return True   # produtivo (4-5 stars)
        else:
            return False  # improdutivo (1-3 stars)
            
    except Exception as e:
        print(f"❌ Erro no modelo NLP: {e}")
        # Em caso de erro, use fallback baseado em palavras-chave positivas
        palavras_produtivas = ['reunião', 'projeto', 'contrato', 'relatório', 'proposta']
        if any(p in texto_lower for p in palavras_produtivas):
            return True
        return False

def gerar_resposta(produtivo):
    if produtivo:
        return "Obrigado pelo envio! Seu email foi classificado como produtivo e será tratado com prioridade."
    else:
        return "Recebemos seu email, mas ele foi classificado como improdutivo. Caso discorde, entre em contato."