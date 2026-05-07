# 🔍 Comparador Liga Magic

Aplicação web feita em **Python + Streamlit** para comparar:

- 📄 Deck (TXT) vs Coleção (CSV)
- 📊 Coleção (CSV) vs Coleção (CSV)

---

## 🎯 Por que esse projeto existe?

Várias vezes estamos em grupos de WhatsApp onde alguém envia a coleção exportada da LigaMagic.

Filtrar manualmente carta por carta para descobrir se temos algo que precisamos é demorado e pouco eficiente.

Este aplicativo resolve exatamente esse problema.

---

# 🚀 Funcionalidades

## 🔁 1) Deck (TXT) vs Coleção (CSV)

Permite verificar:

- Quais cartas do deck você já possui
- Quais cartas faltam na sua coleção
- Resumo total da comparação

---

## 🔁 2) Coleção vs Coleção

Permite comparar duas coleções e identificar:

- Cartas que existem em ambas
- Cartas que existem na Coleção A mas não na B

---

# 🧠 Inteligência do sistema

✔ Detecta automaticamente se a planilha usa:
- `Card (PT)`
- `Card (EN)`

✔ Ignora quantidade do TXT (ex: `4 Lightning Bolt` → considera apenas o nome)

✔ Permite incluir ou ignorar registros com **Extras**

✔ **Alerta de Falso Positivo (//):**
O sistema detecta cartas com nomes compostos (Split cards, Adventurers, etc). Como a LigaMagic pode exportar nomes parciais, o sistema exibe um aviso quando encontra uma carta com `//`.
*Exemplo:* Sua carta 'Brainstorm' pode ser um **'Endwalker // Brainstorm'** (skin), mas o sistema pode ter encontrado um **'Harmonized Trio // Brainstorm'** (criatura com mágica embutida).

✔ Ordenação alfabética automática

---

# 📥 Como gerar os arquivos na LigaMagic

## 📊 Para gerar a Coleção (CSV)

1. Vá até **Coleção**
2. Clique em **Exportar**
3. Em **Configurações de exportação**, selecione:
   - **Padrão LigaMagic CSV**
4. Salve o arquivo

---

## 📄 Para gerar o Deck (TXT)

1. Vá até o seu **Deck**
2. Clique em **Exportar**
3. Selecione:
   - **Arquivo de texto**
4. Salve o arquivo

---

# 🟢 Extras (Foil, Promo, etc)

Você pode escolher:

- ✅ Incluir registros com Extras
- ❌ Ignorar registros com Extras

Quando incluídos:

- Eles aparecem com uma marcação visual
- Ficam no final da listagem
- Mostram a informação detalhada de cada registro

---

# 🌐 Como usar online (sem instalar nada)

O projeto pode ser acessado em:

👉 https://comparadorligamagic.streamlit.app

---

# 🛠 Tecnologias utilizadas

- Python 3
- Streamlit
- Pandas

---

# 📌 Objetivo

Tornar a comparação de coleções da LigaMagic:

- Rápida
- Visual
- Simples
- Sem precisar baixar ou instalar nada

---

Desenvolvido para facilitar a vida da comunidade Magic 🇧🇷
