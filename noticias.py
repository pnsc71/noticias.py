import streamlit as st
import feedparser
from deep_translator import MyMemoryTranslator
import re
import html
from gtts import gTTS
import io

# 1. Configuração
st.set_page_config(page_title="Radar Pro Voice", page_icon="📡", layout="wide")

st.title("📡 Radar Mundial com Voz")

# 2. Funções de Apoio
@st.cache_data(ttl=600)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto))
        return MyMemoryTranslator(source='en-GB', target='pt-PT').translate(texto_limpo)
    except:
        return texto

def falar(texto):
    # Cria o áudio em Português de Portugal (tld='pt')
    tts = gTTS(text=texto, lang='pt', tld='pt')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

# 3. Fontes
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "cor": "🔴", "traduzir": False},
    {"nome": "RTP Notícias", "url": "https://www.rtp.pt/noticias/rss", "cor": "🔵", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "cor": "🟢", "traduzir": False},
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "cor": "🇺🇸", "traduzir": True},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "cor": "🇬🇧", "traduzir": True}
]

# 4. Interface Lateral com Voz
with st.sidebar:
    st.header("🤖 Briefing de Voz")
    if st.button("🔊 Ouvir Resumo"):
        # Recolhe os títulos para o resumo
        briefing_texto = "Aqui está o teu resumo de hoje. "
        for fonte in fontes[:4]: # Usamos as 4 primeiras para não ser muito longo
            feed = feedparser.parse(fonte['url'])
            if feed.entries:
                t = feed.entries[0].title
                t_limpo = traduzir_pt(t) if fonte['traduzir'] else html.unescape(t)
                briefing_texto += f"Na {fonte['nome']}: {t_limpo}. "
        
        st.write(briefing_texto)
        
        # Gera o áudio
        audio_fp = falar(briefing_texto)
        st.audio(audio_fp, format='audio/mp3')
        st.success("Clica no Play para ouvir!")

# 5. Grelha de Notícias (Normal)
col1, col2 = st.columns(2)
for i, fonte in enumerate(fontes):
    coluna = col1 if i % 2 == 0 else col2
    with coluna:
        st.subheader(f"{fonte['cor']} {fonte['nome']}")
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
                st.caption(f"🔗 [Link]({item.link})")
