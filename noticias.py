import streamlit as st
import feedparser

# 1. Configuração para ocupar o ecrã todo (Wide Mode)
st.set_page_config(page_title="Radar Global 360", page_icon="🌍", layout="wide")

st.title("🌍 Radar Global: Últimas de Portugal e do Mundo")
st.markdown("_As últimas 5 notícias de cada fonte em tempo real_")
st.markdown("---")

# 2. Lista expandida de canais
fontes = {
    "RTP Notícias": "https://www.rtp.pt/noticias/rss",
    "Público": "https://www.publico.pt/rss/ultimas",
    "Expresso": "https://expresso.pt/arc/outboundfeeds/rss/",
    "Observador": "https://observador.pt/feed/",
    "Jornal de Negócios": "https://www.jornaldenegocios.pt/rss",
    "Pplware (Tech)": "https://pplware.sapo.pt/feed/",
    "A Bola": "https://www.abola.pt/rss/0"
}

# 3. Função para ler os dados
def ler_ultimas(url, limite=5):
    feed = feedparser.parse(url)
    return feed.entries[:limite]

# 4. Criação da Grelha (Layout)
# Vamos organizar em 2 colunas grandes para ficar bem no Mac e no Telemóvel
col1, col2 = st.columns(2)

# Variável para alternar entre as colunas
contador = 0

for nome, url in fontes.items():
    # Decide em que coluna colocar a fonte atual
    coluna_atual = col1 if contador % 2 == 0 else col2
    
    with coluna_atual:
        st.subheader(f"🗞️ {nome}")
        noticias = ler_ultimas(url)
        
        if not noticias:
            st.warning(f"Não foi possível carregar {nome}")
        
        for item in noticias:
            with st.expander(f"{item.title}"):
                # Se houver data de publicação, mostra
                if hasattr(item, 'published'):
                    st.caption(f"🕒 {item.published}")
                
                # Resumo da notícia
                resumo = item.get('summary', 'Sem resumo disponível.')
                st.markdown(resumo, unsafe_allow_html=True)
                
                # Link
                st.markdown(f"[🔗 Ler no site]({item.link})")
        
        st.markdown("---") # Linha separadora entre jornais
    
    contador += 1

# Rodapé
st.sidebar.title("Configurações")
if st.sidebar.button("Forçar Atualização Geral 🔄"):
    st.rerun()

st.sidebar.info("Este radar organiza automaticamente as notícias em grelha para uma leitura rápida.")
