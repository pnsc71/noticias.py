import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html
from gtts import gTTS
import io

# 1. Configuração
st.set_page_config(page_title="Radar Pro", page_icon="📡", layout="wide")
st.title("📡 Radar Mundial: Portugal & Mundo")

# 2. Função de Tradução Robusta
@st.cache_data(ttl=300)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        # Limpa o lixo antes de enviar para tradução
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto)).strip()
        
        # GoogleTranslator é mais estável que o MyMemory para uso gratuito
        traducao = GoogleTranslator(source='en', target='pt').translate(texto_limpo)
        
        # Pequeno ajuste manual para termos comuns de Portugal
        correcoes = {"equipe": "equipa", "usuário": "utilizador", "tela": "ecrã"}
        for br, pt in correcoes.items():
            traducao = traducao.replace(br, pt)
            
        return traducao
    except Exception as e:
        # Se falhar, devolve o original para a app não dar erro
        return texto

def gerar_audio(texto):
    tts = gTTS(text=texto, lang='pt', tld='pt')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# 3. Fontes
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "cor": "🔴", "traduzir": False},
    {"nome": "RTP Notícias", "url": "https://www.rtp.pt/noticias/rss", "cor": "🔵", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "cor": "🟢", "traduzir": False},
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "cor": "🇺🇸", "traduzir": True},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "cor": "🇬🇧", "traduzir": True}
]

# 4. Sidebar e Voz
with st.sidebar:
    st.header("🤖 Briefing de Voz")
    if st.button("🔊 Gerar Áudio"):
        with st.spinner("A preparar voz..."):
            resumo = "Resumo das notícias. "
            for fonte in fontes[:3]:
                feed = feedparser.parse(fonte['url'])
                if feed.entries:
                    tit = feed.entries[0].title
                    resumo += f"Na {fonte['nome']}: {traduzir_pt(tit) if fonte['traduzir'] else tit}. "
            st.audio(gerar_audio(resumo), format='audio/mp3')

# 5. Grelha Principal
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
