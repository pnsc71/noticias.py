import streamlit as st
import feedparser

# Configuração da página para Mac e Telemóvel
st.set_page_config(page_title="Meu Radar de Notícias", page_icon="🌍", layout="wide")

st.title("🌍 Radar Global em Português")
st.markdown("---")

# Lista de feeds RSS de confiança
canais = {
    "🌍 Geral (RTP)": "https://www.rtp.pt/noticias/rss",
    "💰 Economia (Jornal de Negócios)": "https://www.jornaldenegocios.pt/rss",
    "💻 Tecnologia (Pplware)": "https://pplware.sapo.pt/feed/",
    "⚽ Desporto (A Bola)": "https://www.abola.pt/rss/0"
}

# Barra Lateral
st.sidebar.header("Configurações")
escolha = st.sidebar.selectbox("Selecione o canal:", list(canais.keys()))
num_noticias = st.sidebar.slider("Quantas notícias quer ver?", 5, 30, 10)

# Função para ler os dados do jornal
def ler_feed(url):
    feed = feedparser.parse(url)
    return feed.entries[:num_noticias]

# Botão principal de atualização
if st.button(f"Atualizar {escolha} 🔄"):
    with st.spinner('A consultar os satélites...'):
        noticias = ler_feed(canais[escolha])
        
        if not noticias:
            st.error("Não consegui carregar as notícias. Tente outra fonte.")
        
        for item in noticias:
            # Criamos uma caixa expansível para cada notícia
            with st.expander(f"📌 {item.title}"):
                st.write(f"**Publicado em:** {item.published}")
                st.write("---")
                
                # Vamos buscar o texto (summary) de forma segura
                conteudo = item.get('summary', 'Clique no link para ler o artigo completo.')
                
                # Mostra o conteúdo interpretando as imagens (HTML)
                st.markdown(conteudo, unsafe_allow_html=True)
                
                # Link direto para o jornal
                st.markdown(f"**[🔗 Ler notícia completa no site]({item.link})**")

# Rodapé informativo
st.sidebar.markdown("---")
st.sidebar.info("💡 Este radar filtra publicidade e mostra apenas a informação essencial.")
