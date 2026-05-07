import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Comparador Liga Magic", layout="wide")

# Custom CSS to optimize space and mobile responsiveness
st.markdown("""
    <style>
           /* Reduz margens gerais */
           .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            
            /* Ajustes para telas menores (celular) */
            @media (max-width: 640px) {
                .block-container {
                    padding-left: 0.5rem;
                    padding-right: 0.5rem;
                }
                h1 {
                    font-size: 1.8rem !important;
                }
                h2 {
                    font-size: 1.2rem !important;
                }
            }
            
            /* Remove espaço extra do header do Streamlit */
            header {
                visibility: hidden;
                height: 0;
            }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 Comparador Liga Magic")
st.subheader("Compare Decks e Coleções da LigaMagic")

st.divider()

# =============================
# TOP LAYOUT: INSTRUÇÕES, MODO E OPÇÕES
# =============================
top_col1, top_col2, top_col3 = st.columns([1.5, 1, 1])

with top_col1:
    st.markdown("##### 📘 Instruções")
    with st.expander("Ver passo a passo"):
        st.markdown("""
        **Coleção (CSV):**
        1. Vá até **Coleção** -> **Exportar**
        2. Selecione **Padrão LigaMagic CSV**
        
        **Deck (TXT):**
        1. Vá até o seu **Deck** -> **Exportar**
        2. Selecione **Arquivo de texto**
        """)

with top_col2:
    st.markdown("##### 🔄 Modo")
    modo = st.radio(
        "Comparar:",
        (
            "Deck (TXT) vs Coleção (CSV)",
            "Coleção (CSV) vs Coleção (CSV)"
        ),
        label_visibility="collapsed"
    )

with top_col3:
    st.markdown("##### ⚙️ Opções")
    ANALISAR_EXTRAS = st.checkbox(
        "Incluir 'Extras' (Foil, etc...)",
        value=False
    )

st.divider()

# =============================
# FUNÇÕES
# =============================

def normalizar_nomes(texto: str):
    """
    Normaliza texto e trata cartas com dois nomes usando '//'
    """
    if not isinstance(texto, str):
        return []
        
    partes = texto.split("//")

    nomes = []
    for p in partes:
        n = " ".join(p.lower().strip().split())
        if n:
            nomes.append(n)

    return nomes


def obter_coluna_nome(df, preferencia=None):

    if preferencia and preferencia in df.columns:
        return preferencia

    if "Card (PT)" in df.columns:
        return "Card (PT)"

    if "Card (EN)" in df.columns:
        return "Card (EN)"

    return None


def extrair_nomes_csv(arquivo_csv, coluna_preferida=None):
    try:
        # Tenta ler com utf-8, se falhar tenta latin-1
        try:
            content = arquivo_csv.read().decode("utf-8")
        except UnicodeDecodeError:
            arquivo_csv.seek(0)
            content = arquivo_csv.read().decode("latin-1")
        
        df = pd.read_csv(io.StringIO(content), dtype=str)
        df = df.fillna("")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")
        return []

    coluna_nome = obter_coluna_nome(df, coluna_preferida)

    if not coluna_nome:
        st.error("Coluna 'Card (PT)' ou 'Card (EN)' não encontrada no CSV.")
        return []

    registros = []

    for _, row in df.iterrows():

        nome = str(row[coluna_nome]).strip()
        if not nome:
            continue

        extra = str(row["Extras"]).strip() if "Extras" in df.columns else ""

        if not ANALISAR_EXTRAS and extra:
            continue

        edicao_pt = str(row.get("Edicao (PTBR)", "")).strip()
        edicao_en = str(row.get("Edicao (EN)", "")).strip()
        edicao = edicao_pt if edicao_pt else edicao_en

        detalhes = {
            "Nome Original": nome,
            "Edição": edicao,
            "Quantidade": row.get("Quantidade", ""),
            "Qualidade": row.get("Qualidade (M NM SP MP HP D)", ""),
            "Idioma": row.get("Idioma (BR EN DE ES FR IT JP KO RU TW)", ""),
            "Extra": extra
        }

        nomes = normalizar_nomes(nome)

        for n in nomes:
            registros.append((n, detalhes))

    return registros


def extrair_nomes_txt(txt_file):

    nomes = []

    try:
        linhas = txt_file.read().decode("utf-8").splitlines()
    except UnicodeDecodeError:
        txt_file.seek(0)
        linhas = txt_file.read().decode("latin-1").splitlines()

    for linha in linhas:

        linha = linha.strip()

        if not linha:
            continue

        partes = linha.split(" ", 1)

        if len(partes) > 1:

            nomes_normalizados = normalizar_nomes(partes[1])

            for n in nomes_normalizados:
                nomes.append(n)

    return nomes


def comparar_lista(lista_base, lista_comparacao):
    """
    lista_base: lista de nomes normalizados (strings)
    lista_comparacao: lista de tuples (nome_normalizado, detalhes_dict)
    """

    # Agrupar todos os registros da coleção por nome normalizado
    mapa_colecao = {}
    for nome_norm, detalhes in lista_comparacao:
        if nome_norm not in mapa_colecao:
            mapa_colecao[nome_norm] = []
        mapa_colecao[nome_norm].append(detalhes)

    encontrados = {} # Usar dicionário para garantir unicidade do nome da lista_base
    nao_encontrados = []

    for nome in lista_base:
        if nome in mapa_colecao:
            if nome not in encontrados:
                encontrados[nome] = mapa_colecao[nome]
        else:
            nao_encontrados.append(nome)

    # Converter encontrados para lista ordenada de tuplas (nome, lista_detalhes)
    lista_encontrados = sorted(encontrados.items())
    nao_encontrados = sorted(set(nao_encontrados))

    return lista_encontrados, nao_encontrados


def exibir_encontrados(lista):

    for nome, lista_detalhes in lista:
        
        # Verifica se algum detalhe tem "Extra" para destacar no título
        tem_extra = any(d["Extra"] != "" for d in lista_detalhes)
        
        expander_label = f"{nome.title()}"
        if tem_extra:
            expander_label += " (Contém Extras)"

        with st.expander(expander_label):
            for i, det in enumerate(lista_detalhes):
                
                # Alerta para nomes compostos (Split cards, Adventurers, Skins, etc)
                if "//" in det["Nome Original"]:
                    st.warning(
                        f"⚠️ **Atenção:** Possível falso positivo.\n\n"
                        f"Na coleção consta como: **{det['Nome Original']}**\n\n"
                        f"Isso ocorre porque a LigaMagic exporta nomes compostos separadamente. "
                        f"Por exemplo, a carta 'Brainstorm' pode ser um **'Endwalker // Brainstorm'** "
                        f"(que é uma 'skin' da carta original), mas o sistema pode ter encontrado um "
                        f"**'Harmonized Trio // Brainstorm'** (que é uma criatura com a mágica embutida)."
                    )

                st.markdown(f"**Registro {i+1}:**")
                cols = st.columns(4)
                cols[0].write(f"**Coleção:**\n{det['Edição']}")
                cols[1].write(f"**Qtd:**\n{det['Quantidade']}")
                cols[2].write(f"**Qualidade:**\n{det['Qualidade']}")
                cols[3].write(f"**Idioma:**\n{det['Idioma']}")
                if det["Extra"]:
                    st.info(f"**Extra:** {det['Extra']}")
                if i < len(lista_detalhes) - 1:
                    st.divider()


# =============================
# INTERFACE
# =============================

if modo == "Deck (TXT) vs Coleção (CSV)":

    st.markdown("### 📤 Envie os arquivos")
    up_col1, up_col2 = st.columns(2)

    with up_col1:
        csv_file = st.file_uploader(
            "Arquivo da Coleção (.csv)",
            type=["csv"],
            key="csv1"
        )

    with up_col2:
        txt_file = st.file_uploader(
            "Arquivo do Deck (.txt)",
            type=["txt"],
            key="txt"
        )

    if csv_file and txt_file:

        lista_txt = extrair_nomes_txt(txt_file)

        # Precisamos ler o CSV duas vezes (ou resetar o buffer)
        csv_file.seek(0)
        lista_csv_pt = extrair_nomes_csv(csv_file, "Card (PT)")
        csv_file.seek(0)
        lista_csv_en = extrair_nomes_csv(csv_file, "Card (EN)")

        intersecao_pt = len(set(lista_txt) & set([n for n, _ in lista_csv_pt]))
        intersecao_en = len(set(lista_txt) & set([n for n, _ in lista_csv_en]))

        if intersecao_en > intersecao_pt:
            lista_csv = lista_csv_en
        else:
            lista_csv = lista_csv_pt

        encontrados, nao_encontrados = comparar_lista(lista_txt, lista_csv)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"❌ Não encontrados ({len(nao_encontrados)})")
            st.write(nao_encontrados)

        with col2:
            st.subheader(f"✔ Encontrados ({len(encontrados)})")
            exibir_encontrados(encontrados)

        st.divider()

        st.markdown("### 📊 Resumo")
        st.write(f"Total no Deck: {len(lista_txt)}")
        st.write(f"Não encontrados: {len(nao_encontrados)}")
        st.write(f"Encontrados: {len(encontrados)}")

else:

    st.markdown("### 📤 Envie as duas coleções")
    up_col1, up_col2 = st.columns(2)

    with up_col1:
        csv_a = st.file_uploader(
            "Coleção A (.csv)",
            type=["csv"],
            key="csvA"
        )

    with up_col2:
        csv_b = st.file_uploader(
            "Coleção B (.csv)",
            type=["csv"],
            key="csvB"
        )

    if csv_a and csv_b:

        lista_a = extrair_nomes_csv(csv_a)
        csv_b.seek(0)
        lista_b = extrair_nomes_csv(csv_b)

        encontrados, nao_encontrados = comparar_lista(
            [n for n, _ in lista_a],
            lista_b
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"❌ Só na Coleção A ({len(nao_encontrados)})")
            st.write(nao_encontrados)

        with col2:
            st.subheader(f"✔ Em ambas ({len(encontrados)})")
            exibir_encontrados(encontrados)
