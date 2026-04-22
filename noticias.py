import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html
from gtts import gTTS
import io

# 1. Configuração e Estilo
st.set_page_config(page_title="Radar Pro", page_icon="📡", layout="wide")

# Estética para o iPhone (fundo escuro e botões visíveis)
st.markdown("""
    <style>
    .stAudio { margin-bottom: 20px; }
    .reportview-container { background: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 O Teu Radar: Portugal & Mundo")

# 2. Funções de Apoio (Otimizadas)
@st.cache_data(ttl=300)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto)).strip()
        return GoogleTranslator(source='en', target='pt').translate(texto_limpo)
    except:
        return texto

def gerar_audio(texto):
    tts = gTTS(text=texto, lang='pt', tld='pt')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# 3. Fontes
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "traduzir": False},
    {"nome": "RTP Notícias", "url": "https://www.rtp.pt/noticias/rss", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "traduzir": False},
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "traduzir": True},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "traduzir": True}
]

# --- 4. SECÇÃO "ABRIR E JÁ ESTÁ" (NO TOPO) ---
st.subheader("🤖 O Teu Briefing de Voz")

# Gerar o texto do resumo automaticamente
resumo_completo = "Olá Pedro! Aqui está o essencial de agora. "
for fonte in fontes[:4]:
    feed = feedparser.parse(fonte['url'])
    if feed.entries:
        tit_original = feed.entries[0].title
        tit_final = traduzir_pt(tit_original) if fonte['traduzir'] else html.unescape(tit_original)
        resumo_completo += f"Na {fonte['nome']}, destaca-se: {tit_final}. "

# Mostrar o texto do resumo logo de cara
st.info(resumo_completo)

# Gerar e mostrar o áudio logo abaixo do texto
audio_fp = gerar_audio(resumo_completo)
st.audio(audio_fp, format='audio/mp3')
st.caption("☝️ Carrega no Play para ouvir o resumo")

st.divider()

# --- 5. GRELHA DE NOTÍCIAS DETALHADA ---
col1, col2 = st.columns(2)
for i, fonte in enumerate(fontes):
    coluna = col1 if i % 2 == 0 else col2
    with coluna:
        st.write(f"### {fonte['nome']}")
        feed = feedparser.parse(fonte['url'])
        for item in feed.entries[:5]:
            if fonte['traduzir']:
                titulo = traduzir_pt(item.title)
                resumo = traduzir_pt(item.get('summary', ''))
            else:
                titulo = html.unescape(item.title)
                resumo = html.unescape(item.get('summary', '') or item.get('description', ''))
                resumo = re.sub('<[^<]+?>', '', resumo)

            with st.expander(f"📌 {titulo}"):
                st.write(resumo)
                st.caption(f"[Notícia completa]({item.link})")
