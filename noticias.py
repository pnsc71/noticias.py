import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html

# 1. Configuração e CSS Avançado
st.set_page_config(page_title="Radar Elite", page_icon="📡", layout="wide")

st.markdown("""
    <style>
    .breaking-card {
        background-color: #2d0a0a;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ff4b4b;
        margin-bottom: 20px;
    }
    .news-card {
        background-color: #1e212b;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 4px solid #007bff;
        margin-bottom: 20px;
    }
    .img-container img {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 10px;
        object-fit: cover;
        max-height: 200px;
    }
    .tag {
        padding: 4px 8px;
        border-radius: 5px;
        font-size: 10px;
        font-weight: bold;
        background: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Funções de Suporte
@st.cache_data(ttl=300)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto)).strip()
        return GoogleTranslator(source='en', target='pt').translate(texto_limpo)
    except: return texto

def extrair_imagem(item):
    # Tenta encontrar imagem no feed (vários formatos possíveis)
    if 'links' in item:
        for link in item.links:
            if 'image' in link.get('type', ''): return link.href
    if 'media_content' in item:
        return item.media_content[0]['url']
    if 'description' in item:
        img_match = re.search(r'<img src="([^"]+)"', item.description)
        if img_match: return img_match.group(1)
    return "https://via.placeholder.com/400x200?text=Radar+News"

# 3. Definição das Fontes e Temas
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "tema": "Geral", "traduzir": False},
    {"nome": "A Bola", "url": "https://www.abola.pt/rss/0", "tema": "Desporto", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "tema": "Tech", "traduzir": False},
    {"nome": "Público", "url": "https://www.publico.pt/rss/politica", "tema": "Política", "traduzir": False},
    {"nome": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "tema": "Mundo", "traduzir": True}
]

# --- 4. INTERFACE E FILTROS ---
st.title("🛰️ Radar Elite v3.0")

# Filtros por tema
temas = ["Tudo", "Geral", "Desporto", "Tech", "Política", "Mundo"]
filtro = st.radio("Escolhe o que queres ver:", temas, horizontal=True)

st.divider()

# --- 5. PROCESSAMENTO E EXIBIÇÃO ---
all_items = []

for f in fontes:
    if filtro != "Tudo" and f['tema'] != filtro:
        continue
    
    feed = feedparser.parse(f['url'])
    for entry in feed.entries[:5]:
        entry['fonte_nome'] = f['nome']
        entry['precisa_traducao'] = f['traduzir']
        all_items.append(entry)

# Ordenar por data (opcional, se o feed tiver data válida)
# all_items.sort(key=lambda x: x.get('published_parsed'), reverse=True)

cols = st.columns(2)

for i, item in enumerate(all_items):
    col = cols[i % 2]
    
    # 1. Tradução e Limpeza
    titulo = traduzir_pt(item.title) if item['precisa_traducao'] else html.unescape(item.title)
    resumo = traduzir_pt(item.get('summary', '')) if item['precisa_traducao'] else html.unescape(item.get('summary', '') or "")
    resumo = re.sub('<[^<]+?>', '', resumo)[:120] + "..."
    
    # 2. Imagem
    img_url = extrair_imagem(item)
    
    # 3. Lógica de "Breaking News"
    palavras_alerta = ["URGENTE", "ÚLTIMA HORA", "BOMBA", "BREAKING"]
    is_breaking = any(p in titulo.upper() for p in palavras_alerta)
    card_class = "breaking-card" if is_breaking else "news-card"
    alerta_label = "🚨 BREAKING" if is_breaking else item['fonte_nome']

    with col:
        st.markdown(f"""
            <div class="{card_class}">
                <div class="img-container"><img src="{img_url}"></div>
                <span class="tag">{alerta_label}</span>
                <h4 style="margin-top:10px;">{titulo}</h4>
                <p style="font-size: 13px; color: #bbb;">{resumo}</p>
                <a href="{item.link}" target="_blank" style="color: #00d4ff; text-decoration: none;">Ler mais →</a>
            </div>
            """, unsafe_allow_html=True)
