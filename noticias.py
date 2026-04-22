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
# 4. Sidebar e Voz (Versão simplificada para iPhone)
with st.sidebar:
    st.header("🤖 Briefing de Voz")
    
    # Criamos um botão simples. No iPhone, menos é mais.
    if st.button("🔊 Gerar Áudio"):
        resumo_texto = "Olá Pedro. Aqui tens o resumo. "
        
        # Vamos buscar apenas os 3 primeiros títulos para ser rápido
        for fonte in fontes[:3]:
            feed = feedparser.parse(fonte['url'])
            if feed.entries:
                t_raw = feed.entries[0].title
                t_pt = traduzir_pt(t_raw) if fonte['traduzir'] else html.unescape(t_raw)
                resumo_texto += f"Na {fonte['nome']}: {t_pt}. "
        
        # Gerar o áudio
        audio_data = gerar_audio(resumo_texto)
        
        # Exibir o leitor
        st.audio(audio_data, format='audio/mp3')
        st.success("Áudio pronto! Clica no Play.")

    st.divider()
    st.caption("Nota: No iPhone, desliga o botão lateral do silêncio (laranja) para o som sair.")

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
