import streamlit as st
import feedparser

# Configuração da página
st.set_page_config(page_title="Meu Radar de Notícias", page_icon="🌍")

st.title("🌍 Radar Global em Português")
st.markdown("---")

# Lista de feeds RSS de confiança
canais = {
    "🌍 Geral (RTP)": "https://www.rtp.pt/noticias/rss",
    "💰 Economia (Jornal de Negócios)": "https://www.jornaldenegocios.pt/rss",
    "💻 Tecnologia (Pplware)": "https://pplware.sapo.pt/feed/",
    "⚽ Desporto (A Bola)": "https://www.abola.pt/rss/0"
}

# Barra Lateral para escolha
st.sidebar.header("Configurações")
escolha = st.sidebar.selectbox("Selecione o canal:", list(canais.keys()))
num_noticias = st.sidebar.slider("Quantas notícias quer ver?", 5, 20, 10)

# Função para ler os dados
def ler_feed(url):
    feed = feedparser.parse(url)
    return feed.entries[:num_noticias]

# Botão principal
if st.button(f"Atualizar {escolha} 🔄"):
    with st.spinner('A consultar os satélites...'):
        noticias = ler_feed(canais[escolha])
        
        if not noticias:
            st.error("Não consegui carregar as notícias. Tente outra fonte.")
        
        for item in noticias:
            with st.expander(f"📌 {item.title}"):
                st.markdown(resumo, unsafe_allow_html=True)
                st.write("---")
                # Alguns feeds mandam um resumo (summary), outros não
                resumo = item.get('summary', 'Clique no link para ler o artigo completo.')
                st.write(resumo)
                st.markdown(f"[🔗 Ler notícia no site]({item.link})")

st.sidebar.markdown("---")
st.sidebar.write("💡 **Dica:** Use o slider acima para controlar o tamanho da sua lista de leitura.")
