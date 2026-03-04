# 🔍 Comparador Liga Magic

Aplicação web para comparar automaticamente um **Deck (TXT)** com sua **Coleção (XLS - padrão LigaMagic)**.

A ferramenta verifica carta por carta e informa:

- ❌ Quais cartas do deck NÃO existem na coleção
- ✔ Quais cartas existem na coleção
- 📊 Resumo total da comparação

---

## 🎯 Por que esse projeto existe?

Várias vezes nós estamos em grupos onde a pessoa manda a coleção e fica difícil filtrar manualmente carta por carta que precisamos.

Fazer essa comparação manualmente é:

- Demorado
- Sujeito a erro
- Cansativo

Esse aplicativo resolve exatamente esse problema de forma automática e instantânea.

---

## 🚀 Como usar

Acesse a aplicação online e faça upload de:

- 📘 Arquivo da Coleção (.xls) exportado da LigaMagic
- 📗 Arquivo do Deck (.txt) exportado da LigaMagic

O sistema faz a comparação imediatamente.

---

## 📘 Como gerar o arquivo da Coleção (Excel)

1. Vá até **Coleção**
2. Clique em **Exportar**
3. Em **Configurações de exportação** selecione:
   - **Padrão LigaMagic XLS**
4. Gere e salve o arquivo

---

## 📗 Como gerar o arquivo do Deck (TXT)

1. Vá até o seu **Deck**
2. Clique em **Exportar**
3. Selecione:
   - **Arquivo de texto**
4. Salve o arquivo

---

## ⚙️ Regras da Comparação

- A quantidade de cartas é ignorada
- A comparação é exata (evita falso positivo como `Charge` vs `Inspired Charge`)
- Pode opcionalmente ignorar linhas que possuem conteúdo na coluna `Extras` (Cartas Foil e etc..)
- Resultados são ordenados alfabeticamente

---

## 🛠 Tecnologias Utilizadas

- Python
- Streamlit
- Pandas

---

## 💡 Possíveis Melhorias Futuras

- Exportar resultado em Excel
- Melhorias de performance para coleções grandes
- Interface aprimorada

---

## 📄 Licença

Projeto de uso livre.
