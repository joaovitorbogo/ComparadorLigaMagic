import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador Liga Magic", layout="wide")

st.title("🔍 Comparador Liga Magic")
st.subheader("Compare Decks e Coleções da LigaMagic")

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
    "Analisar linhas que possuem conteúdo na coluna 'Extras'?",
    value=False
)

st.divider()


# =============================
# FUNÇÕES AUXILIARES
# =============================

def normalizar(texto: str) -> str:
    return " ".join(texto.lower().strip().split())


def extrair_nomes_excel(arquivo_excel):
    df = pd.read_excel(arquivo_excel, dtype=str, engine="openpyxl")
    df = df.fillna("")

    if not ANALISAR_EXTRAS:
        if "Extras" not in df.columns:
            st.error("Coluna 'Extras' não encontrada no Excel.")
            return []
        df = df[df["Extras"].str.strip() == ""]

    todas_celulas = df.astype(str).values.flatten()

    nomes = []
    for celula in todas_celulas:
        celula = normalizar(celula)
        if celula:
            nomes.append(celula)

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
    encontrados = []
    nao_encontrados = []

    for nome in lista_base:
        palavras_base = nome.split()
        encontrou = False

        for outro in lista_comparacao:
            palavras_outro = outro.split()
            if len(palavras_base) == len(palavras_outro) and nome == outro:
                encontrou = True
                break

        if encontrou:
            encontrados.append(nome)
        else:
            nao_encontrados.append(nome)

    encontrados = sorted(set(encontrados))
    nao_encontrados = sorted(set(nao_encontrados))

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
        lista_excel = extrair_nomes_excel(excel_file)
        lista_txt = extrair_nomes_txt(txt_file)

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

        st.divider()
        st.markdown("### 📊 Resumo")
        st.write(f"Total na Coleção A: {len(lista_a)}")
        st.write(f"Exclusivas da A: {len(nao_encontrados)}")
        st.write(f"Presentes em ambas: {len(encontrados)}")
