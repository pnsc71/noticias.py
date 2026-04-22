import streamlit as st
import feedparser
from googletrans import Translator
import re

# 1. Configuração
st.set_page_config(page_title="Radar Mundial pt-PT", page_icon="📡", layout="wide")

# Inicializa o Tradutor
tradutor = Translator()

# 2. Função de Tradução Melhorada para pt-PT
@st.cache_data(ttl=600)
def traduzir(texto):
    if not texto: return ""
    try:
        # Limpa HTML
        texto_limpo = re.sub('<[^<]+?>', '', texto)
        # Forçamos o destino para 'pt' (embora o Google tente decidir o sotaque)
        # Infelizmente o Google às vezes teima no BR, mas esta biblioteca é mais precisa
        resultado = tradutor.translate(texto_limpo, dest='pt')
        return resultado.text
    except:
        return texto

# --- RESTO DO CÓDIGO IGUAL AO ANTERIOR ---
# (Podes manter a lógica das colunas e fontes que já tinhas)
