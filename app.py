import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador MTG", layout="wide")

st.title("Comparador de Deck vs Coleção")

ANALISAR_EXTRAS = st.checkbox("Analisar linhas que possuem conteúdo na coluna 'Extras'?", value=False)


def normalizar(texto: str) -> str:
    return " ".join(texto.lower().strip().split())


def processar(excel_file, txt_file):
    df = pd.read_excel(excel_file, dtype=str, engine="openpyxl")
    df = df.fillna("")

    if not ANALISAR_EXTRAS:
        if "Extras" not in df.columns:
            st.error("Coluna 'Extras' não encontrada no Excel.")
            return
        df = df[df["Extras"].str.strip() == ""]

    todas_celulas = df.astype(str).values.flatten()
    celulas_normalizadas = [
        normalizar(c) for c in todas_celulas if c.strip()
    ]

    nomes = []
    linhas_txt = txt_file.read().decode("utf-8").splitlines()

    for linha in linhas_txt:
        linha = linha.strip()
        if not linha:
            continue

        partes = linha.split(" ", 1)
        if len(partes) > 1:
            nomes.append(normalizar(partes[1]))

    encontrados = []
    nao_encontrados = []

    for nome in nomes:
        palavras_txt = nome.split()
        encontrou = False

        for celula in celulas_normalizadas:
            palavras_excel = celula.split()
            if len(palavras_excel) == len(palavras_txt) and celula == nome:
                encontrou = True
                break

        if encontrou:
            encontrados.append(nome)
        else:
            nao_encontrados.append(nome)

    encontrados.sort()
    nao_encontrados.sort()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("❌ Não encontrados")
        st.write(nao_encontrados)

    with col2:
        st.subheader("✔ Encontrados")
        st.write(encontrados)

    st.divider()
    st.write(f"Total no TXT: {len(nomes)}")
    st.write(f"Não encontrados: {len(nao_encontrados)}")
    st.write(f"Encontrados: {len(encontrados)}")


excel_file = st.file_uploader("Envie o Excel (.xls ou .xlsx)", type=["xls", "xlsx"])
txt_file = st.file_uploader("Envie o TXT", type=["txt"])

if excel_file and txt_file:
    processar(excel_file, txt_file)