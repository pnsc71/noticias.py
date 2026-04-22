import streamlit as st
import feedparser

# 1. Configuração para ocupar o ecrã todo
st.set_page_config(page_title="Radar Notícias Portugal", page_icon="🌍", layout="wide")

st.title("🌍 Radar Global: Centro de Comando")
st.markdown("_As últimas 5 notícias de fontes em tempo real_")
st.markdown("---")

# 2. Lista de fontes atualizada e testada
fontes = {
    "SIC Notícias": "https://sicnoticias.pt/feed",
    "CNN Portugal": "https://cnnportugal.iol.pt/rss",
    "RTP Notícias": "https://www.rtp.pt/noticias/rss",
    "Observador": "https://observador.pt/feed/",
    "O Jogo": "https://www.ojogo.pt/rss",
    "A Bola": "https://www.abola.pt/rss/0",
    "Jornal de Negócios": "https://www.jornaldenegocios.pt/rss",
    "Pplware (Tech)": "https://pplware.sapo.pt/feed/"
}

# 3. Função para ler os dados
def ler_ultimas(url, limite=5):
    # Forçamos um "User-Agent" para o jornal não nos bloquear
    feed = feedparser.parse(url)
    return feed.entries[:limite]

# 4. Criação da Grelha (Layout em 2 colunas)
col1, col2 = st.columns(2)

contador = 0

for nome, url in fontes.items():
    coluna_atual = col1 if contador % 2 == 0 else col2
    
    with coluna_atual:
        st.subheader(f"🗞️ {nome}")
        noticias = ler_ultimas(url)
        
        if not noticias:
            st.info(f"Fonte {nome} temporariamente indisponível.")
        
        for item in noticias:
            # Usamos o título como botão do expander
            with st.expander(f"{item.title}"):
                if hasattr(item, 'published'):
                    st.caption(f"🕒 {item.published}")
                
                # Vamos buscar o resumo ou descrição
                resumo = item.get('summary', '')
                if not resumo and 'description' in item:
                    resumo = item.description
                
                # Limpeza e exibição
                st.markdown(resumo, unsafe_allow_html=True)
                st.markdown(f"**[🔗 Ler notícia completa]({item.link})**")
        
        st.markdown("<br>", unsafe_allow_html=True) # Espaço extra entre jornais
    
    contador += 1

# Barra Lateral
st.sidebar.title("Configurações")
st.sidebar.write("O radar atualiza automaticamente ao abrir.")
if st.sidebar.button("Atualizar Agora 🔄"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 Este layout foi desenhado para visualização rápida em grelha.")
