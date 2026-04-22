import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html

# 1. Configuração e Estilo
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
        height: 180px;
    }
    .tag {
        padding: 4px 8px;
        border-radius: 5px;
        font-size: 10px;
        font-weight: bold;
        background: #333;
        color: white;
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
    try:
        if 'media_content' in item and item.media_content:
            return item.media_content[0]['url']
        if 'links' in item:
            for link in item.links:
                if 'image' in link.get('type', '') or 'thumbnail' in link.get('rel', ''):
                    return link.href
        full_text = item.get('description', '') + item.get('summary', '')
        img_match = re.search(r'<img src="([^"]+)"', full_text)
        if img_match: return img_match.group(1)
    except: pass
    return "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=400&h=200&q=80"

# 3. Definição das Fontes
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "tema": "Geral", "traduzir": False},
    {"nome": "A Bola", "url": "https://www.abola.pt/rss/0", "tema": "Desporto", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "tema": "Tech", "traduzir": False},
    {"nome": "Público", "url": "https://www.publico.pt/rss/politica", "tema": "Política", "traduzir": False},
    {"nome": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "tema": "Mundo", "traduzir": True}
]

# 4. Título e Filtros
st.title("🛰️ Radar Elite")
temas = ["Tudo", "Geral", "Desporto", "Tech", "Política", "Mundo"]
filtro = st.radio("Filtrar por:", temas, horizontal=True)

st.divider()

# 5. Agregação de Notícias
all_items = []
for f in fontes:
    if filtro == "Tudo" or f['tema'] == filtro:
        feed = feedparser.parse(f['url'])
        for entry in feed.entries[:5]:
            entry['fonte_nome'] = f['nome']
            entry['precisa_traducao'] = f['traduzir']
            all_items.append(entry)

# 6. Exibição em Grelha
if all_items:
    cols = st.columns(2)
    for i, item in enumerate(all_items):
        col_idx = i % 2
        with cols[col_idx]:
            # Tradução e Limpeza
            titulo = traduzir_pt(item.title) if item['precisa_traducao'] else html.unescape(item.title)
            resumo_raw = item.get('summary', '') or item.get('description', '')
            resumo = traduzir_pt(resumo_raw) if item['precisa_traducao'] else html.unescape(resumo_raw)
            resumo = re.sub('<[^<]+?>', '', resumo)[:120] + "..."
            
            img_url = extrair_imagem(item)
            
            # Alerta Breaking News
            palavras_alerta = ["URGENTE", "ÚLTIMA HORA", "BOMBA", "BREAKING"]
            is_breaking = any(p in titulo.upper() for p in palavras_alerta)
            card_class = "breaking-card" if is_breaking else "news-card"
            label = "🚨 URGENTE" if is_breaking else item['fonte_nome']

            st.markdown(f"""
                <div class="{card_class}">
                    <div class="img-container">
                        <img src="{img_url}" onerror="this.onerror=null;this.src='https://via.placeholder.com/400x200?text=Notícia';">
                    </div>
                    <span class="tag">{label}</span>
                    <h4 style="margin-top:10px;">{titulo}</h4>
                    <p style="font-size: 13px; color: #bbb;">{resumo}</p>
                    <a href="{item.link}" target="_blank" style="color: #00d4ff; text-decoration: none;">Ler notícia →</a>
                </div>
                """, unsafe_allow_html=True)
else:
    st.warning("Nenhuma notícia encontrada para este tema.")
