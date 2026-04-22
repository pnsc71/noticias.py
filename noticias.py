def extrair_imagem(item):
    try:
        # 1. Tenta no campo media_content (Pplware, CNN)
        if 'media_content' in item and item.media_content:
            return item.media_content[0]['url']
        
        # 2. Tenta nos links (Enclosures)
        if 'links' in item:
            for link in item.links:
                if 'image' in link.get('type', '') or 'thumbnail' in link.get('rel', ''):
                    return link.href
        
        # 3. Tenta dentro da descrição/resumo (Público, A Bola)
        full_text = item.get('description', '') + item.get('summary', '')
        img_match = re.search(r'<img src="([^"]+)"', full_text)
        if img_match:
            url = img_match.group(1)
            # Remove parâmetros de redimensionamento que podem quebrar o link
            if '?' in url and 'abola' in url: url = url.split('?')[0]
            return url

        # 4. Tenta no campo thumbnail
        if 'media_thumbnail' in item and item.media_thumbnail:
            return item.media_thumbnail[0]['url']
            
    except:
        pass
    
    # Se tudo falhar, usa uma imagem neutra de tecnologia/notícias
    return "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=400&h=200&q=80"

# --- NO BLOCO DE EXIBIÇÃO (dentro do loop dos cards) ---
# Substitui a parte da imagem por este código que lida com erros de carregamento:

with col:
    st.markdown(f"""
        <div class="{card_class}">
            <div class="img-container">
                <img src="{img_url}" onerror="this.onerror=null;this.src='https://via.placeholder.com/400x200?text=Radar+News';">
            </div>
            <span class="tag">{alerta_label}</span>
            <h4 style="margin-top:10px;">{titulo}</h4>
            <p style="font-size: 13px; color: #bbb;">{resumo}</p>
            <a href="{item.link}" target="_blank" style="color: #00d4ff; text-decoration: none;">Ler mais →</a>
        </div>
        """, unsafe_allow_html=True)
