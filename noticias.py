import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html

# 1. Configuração e Design do Dashboard
st.set_page_config(page_title="Radar Elite", page_icon="📡", layout="wide")

# Imagem fixa para dar consistência visual (Mundo Digital/Notícias)
IMAGEM_FIXA = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&h=300&q=80"

st.markdown(f"""
    <style>
    /* Estilo dos Cards */
    .news-card {{
        background-color: #1e212b;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 4px solid #007bff;
        margin-bottom: 20px;
        min-height: 400px;
    }}
    /* Estilo para Breaking News */
    .breaking-card {{
        background-color: #2d0a0a;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ff4b4b;
        margin-bottom: 20px;
        min-height: 400px;
    }}
    .img-container img {{
        width: 100%;
        border-radius: 10px;
        margin-bottom: 15px;
        object-fit: cover;
        height: 180px;
    }}
    .tag {{
        padding: 4px 10px;
        border-radius: 5px;
        font-size: 11px;
        font-weight: bold;
        background: #333;
        color: white;
        text-transform: uppercase;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Motor de Tradução
@st.cache_data(ttl=300)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto)).strip()
        return GoogleTranslator(source='en', target='pt').translate(texto_limpo)
    except: return texto

# 3. Fontes de Dados
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "tema": "Geral", "traduzir": False},
    {"nome": "A Bola", "url": "https://www.abola.pt/rss/0", "tema": "Desporto", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "tema": "Tech", "traduzir": False},
    {"nome": "Público", "url": "https://www.publico.pt/rss/politica", "tema": "Política", "traduzir": False},
    {"nome": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "tema": "Mundo", "traduzir": True}
]

# 4. Título e Filtros (Menu Horizontal)
st.title("🛰️ Radar Elite")
temas = ["Tudo", "Geral", "Desporto", "Tech", "Política", "Mundo"]
filtro = st.radio("Filtrar conteúdo:", temas, horizontal=True)

st.divider()

# 5. Agregação de Notícias
all_items = []
for f in fontes:
    if filtro == "Tudo" or f['tema'] == filtro:
        feed = feedparser.parse(f['url'])
        for entry in feed.entries[:6]: # 6 notícias por fonte
            entry['fonte_nome'] = f['nome']
            entry['precisa_traducao'] = f['traduzir']
            all_items.append(entry)

# 6. Exibição em Grelha (2 Colunas)
if all_items:
    cols = st.columns(2)
    for i, item in enumerate(all_items):
        col_idx = i % 2
        with cols[col_idx]:
            # Processamento de Texto
            titulo = traduzir_pt(item.title) if item['precisa_traducao'] else html.unescape(item.title)
            resumo_raw = item.get('summary', '') or item.get('description', '')
            resumo = traduzir_pt(resumo_raw) if item['precisa_traducao'] else html.unescape(resumo_raw)
            resumo = re.sub('<[^<]+?>', '', resumo)[:130] + "..."
            
            # Lógica de Alerta
            palavras_alerta = ["URGENTE", "ÚLTIMA HORA", "BOMBA", "BREAKING"]
            is_breaking = any(p in titulo.upper() for p in palavras_alerta)
            card_class = "breaking-card" if is_breaking else "news-card"
            label = "🚨 URGENTE" if is_breaking else item['fonte_nome']

            # Renderização do Card
            st.markdown(f"""
                <div class="{card_class}">
                    <div class="img-container">
                        <img src="{IMAGEM_FIXA}">
                    </div>
                    <span class="tag">{label}</span>
                    <h4 style="margin-top:12px; min-height: 60px;">{titulo}</h4>
                    <p style="font-size: 14px; color: #bbb;">{resumo}</p>
                    <a href="{item.link}" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">Ler notícia completa →</a>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("A atualizar fontes... tenta outro filtro.")
