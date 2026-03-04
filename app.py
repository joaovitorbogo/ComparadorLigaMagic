import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador Liga Magic", layout="wide")

st.title("🔍 Comparador Liga Magic")
st.subheader("Compare Decks e Coleções da LigaMagic")

st.divider()

# =============================
# INSTRUÇÕES
# =============================

with st.expander("📘 Como gerar o arquivo da Coleção (Excel)", expanded=False):
    st.markdown("""
    **Passo a passo:**
    
    1. Vá até **Coleção**
    2. Clique em **Exportar**
    3. Em **Configurações de exportação** selecione:
       - **Padrão LigaMagic XLS**
    4. Gere o arquivo e salve no seu dispositivo
    """)

with st.expander("📗 Como gerar o arquivo do Deck (TXT)", expanded=False):
    st.markdown("""
    **Passo a passo:**
    
    1. Vá até o seu **Deck**
    2. Clique em **Exportar**
    3. Selecione:
       - **Arquivo de texto**
    4. Salve o arquivo no seu dispositivo
    """)

st.divider()

# =============================
# MODO DE COMPARAÇÃO
# =============================

modo = st.radio(
    "Selecione o tipo de comparação:",
    (
        "Deck (TXT) vs Coleção (XLS)",
        "Coleção (XLS) vs Coleção (XLS)"
    )
)

st.divider()

ANALISAR_EXTRAS = st.checkbox(
    "Analisar linhas que possuem conteúdo na coluna 'Extras' (Foil, etc...)",
    value=False
)

st.divider()


# =============================
# FUNÇÕES AUXILIARES
# =============================

def normalizar(texto: str) -> str:
    return " ".join(texto.lower().strip().split())


def obter_coluna_nome(df, preferencia=None):
    if preferencia and preferencia in df.columns:
        return preferencia

    if "Card (PT)" in df.columns:
        return "Card (PT)"
    if "Card (EN)" in df.columns:
        return "Card (EN)"

    return None


def extrair_nomes_excel(arquivo_excel, coluna_preferida=None):
    df = pd.read_excel(arquivo_excel, dtype=str, engine="openpyxl")
    df = df.fillna("")

    if not ANALISAR_EXTRAS and "Extras" in df.columns:
        df = df[df["Extras"].str.strip() == ""]

    coluna_nome = obter_coluna_nome(df, coluna_preferida)

    if not coluna_nome:
        st.error("Coluna 'Card (PT)' ou 'Card (EN)' não encontrada.")
        return []

    nomes = [
        normalizar(nome)
        for nome in df[coluna_nome].tolist()
        if str(nome).strip()
    ]

    return nomes


def extrair_nomes_txt(txt_file):
    nomes = []
    linhas = txt_file.read().decode("utf-8").splitlines()

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        partes = linha.split(" ", 1)
        if len(partes) > 1:
            nomes.append(normalizar(partes[1]))

    return nomes


def comparar_lista(lista_base, lista_comparacao):
    set_comparacao = set(lista_comparacao)

    encontrados = sorted(set([n for n in lista_base if n in set_comparacao]))
    nao_encontrados = sorted(set([n for n in lista_base if n not in set_comparacao]))

    return encontrados, nao_encontrados


# =============================
# INTERFACE
# =============================

if modo == "Deck (TXT) vs Coleção (XLS)":

    st.markdown("### 📤 Envie os arquivos")

    excel_file = st.file_uploader(
        "Arquivo da Coleção (.xls ou .xlsx)",
        type=["xls", "xlsx"],
        key="excel1"
    )

    txt_file = st.file_uploader(
        "Arquivo do Deck (.txt)",
        type=["txt"],
        key="txt"
    )

    if excel_file and txt_file:

        lista_txt = extrair_nomes_txt(txt_file)

        lista_excel_pt = extrair_nomes_excel(excel_file, "Card (PT)")
        lista_excel_en = extrair_nomes_excel(excel_file, "Card (EN)")

        intersecao_pt = len(set(lista_txt) & set(lista_excel_pt))
        intersecao_en = len(set(lista_txt) & set(lista_excel_en))

        if intersecao_en > intersecao_pt:
            lista_excel = lista_excel_en
        else:
            lista_excel = lista_excel_pt

        encontrados, nao_encontrados = comparar_lista(lista_txt, lista_excel)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("❌ Não encontrados na coleção")
            st.write(nao_encontrados)

        with col2:
            st.subheader("✔ Encontrados na coleção")
            st.write(encontrados)

        st.divider()
        st.markdown("### 📊 Resumo")
        st.write(f"Total no Deck: {len(lista_txt)}")
        st.write(f"Não encontrados: {len(nao_encontrados)}")
        st.write(f"Encontrados: {len(encontrados)}")


else:  # Coleção vs Coleção

    st.markdown("### 📤 Envie as duas coleções")

    excel_a = st.file_uploader(
        "Coleção A (.xls ou .xlsx)",
        type=["xls", "xlsx"],
        key="excelA"
    )

    excel_b = st.file_uploader(
        "Coleção B (.xls ou .xlsx)",
        type=["xls", "xlsx"],
        key="excelB"
    )

    if excel_a and excel_b:

        lista_a = extrair_nomes_excel(excel_a)
        lista_b = extrair_nomes_excel(excel_b)

        encontrados, nao_encontrados = comparar_lista(lista_a, lista_b)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("❌ Existem na Coleção A mas NÃO na B")
            st.write(nao_encontrados)

        with col2:
            st.subheader("✔ Existem em ambas as coleções")
            st.write(encontrados)
