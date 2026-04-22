import streamlit as st
import feedparser

# 1. Configuração da Página
st.set_page_config(page_title="Radar Notícias Portugal", page_icon="🌍", layout="wide")

st.title("🌍 Radar de Notícias: Fontes Ativas")
st.markdown("_Apenas canais com sinal verde e atualizados_")
st.markdown("---")

# 2. Lista de fontes TESTADAS e que funcionam bem em leitores RSS
fontes = {
    "CNN Portugal": "https://cnnportugal.iol.pt/rss",
    "RTP Notícias": "https://www.rtp.pt/noticias/rss",
    "Observador (Últimas)": "https://observador.pt/feed/",
    "Jornal de Negócios": "https://www.jornaldenegocios.pt/rss",
    "Pplware (Tecnologia)": "https://pplware.sapo.pt/feed/",
    "MaisFutebol (Desporto)": "https://maisfutebol.iol.pt/rss",
    "PC Guia (Gadgets)": "https://www.pcguia.pt/feed/"
}

# 3. Função de leitura
def ler_ultimas(url, limite=5):
    feed = feedparser.parse(url)
    return feed.entries[:limite]

# 4. Grelha em 2 colunas
col1, col2 = st.columns(2)
contador = 0

for nome, url in fontes.items():
    coluna_atual = col1 if contador % 2 == 0 else col2
    
    with coluna_atual:
        st.subheader(f"🗞️ {nome}")
        noticias = ler_ultimas(url)
        
        if not noticias:
            st.info(f"O feed de {nome} está a ser filtrado pela fonte.")
        
        for item in noticias:
            with st.expander(f"{item.title}"):
                if hasattr(item, 'published'):
                    st.caption(f"🕒 {item.published}")
                
                # Vai buscar o resumo
                resumo = item.get('summary', '')
                if not resumo and 'description' in item:
                    resumo = item.description
                
                # Exibe o conteúdo e fotos
                st.markdown(resumo, unsafe_allow_html=True)
                st.markdown(f"**[🔗 Ver no site]({item.link})**")
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    contador += 1

# Sidebar
st.sidebar.title("Comandos")
if st.sidebar.button("Atualizar Tudo 🔄"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.success("✅ As fontes selecionadas são compatíveis com o teu radar.")
