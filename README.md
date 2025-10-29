# 🧠 Desafio Técnico — API de Classificação de Saúde

Este repositório contém a solução completa para um **desafio técnico de Machine Learning**.
O objetivo foi **construir um pipeline funcional de ponta a ponta**, capaz de ler, processar e interpretar históricos de chat clínico para **identificar condições de saúde** dos clientes — tudo integrado a uma **API Flask pronta para consumo.**

---

## 🎯 O Desafio

O objetivo deste desafio foi desenvolver um modelo de NLP capaz de **identificar condições de saúde** (como Obesidade, Diabetes, etc.) com base no histórico de mensagens de um cliente.

A entrega principal é uma **API Flask** que recebe um `client_id`, consulta o modelo e retorna uma lista das condições previstas, tratando também casos de `404 Not Found` para clientes inexistentes.

Conforme a expectativa do desafio, o foco principal  **demonstrar um processo claro de investigação**, tomada de decisão e a construção de um pipeline *end-to-end* funcional.

---

## 💡 Abordagem e Pipeline de Dados

O projeto foi desenvolvido seguindo uma **linha lógica de investigação e prototipagem rápida**, priorizando clareza e reprodutibilidade.

### 1\. 🔍 Exploração e Pré-Processamento (EDA)

  - **Análise de relacionamentos** entre os CSVs (`client`, `chat_history`, `client_conditions`, `seed_*`), mapeando chaves e integridades.
  - **Identificação do alvo (`y`)**: o arquivo `client_conditions.csv` foi definido como rótulo do modelo.
  - **Entendimento dos dicionários (`seed_*`)**: interpretados como tabelas de referência, úteis para enriquecer e validar as condições de saúde.

### 2\. 🧱 Engenharia de Features (Preparação do X)

  - Para preservar o contexto do diálogo, as mensagens foram **ordenadas por data** e **prefixadas** com o remetente (`client:` ou `user:`).
  - Todas as mensagens de um cliente foram **concatenadas** em um único documento textual — resultando em uma representação contextualizada e sem ruído.
  - Esse texto passou por **vetorização com TF-IDF**, otimizando a entrada para o modelo.

### 3\. 🎯 Preparação do Alvo (Preparação do y)

  - O dataset de condições foi convertido de formato *longo* para *wide*, via `pandas.crosstab`, gerando um **DataFrame multi-rótulo** (cada coluna = uma condição binária).
  - Exemplo:
    ```
    client_id | e66 | g47 | z72
         1    |  1  |  0  |  1
    ```

-----

## ⚠️ Insight Principal e Tomada de Decisão

Durante a exploração, identificou-se uma limitação crítica:

| Tipo de Dado | Nº de Clientes |
| :--- | :---: |
| Histórico de Chat (`X`) | 3 |
| Condições (`y`) | 2 |
| Interseção útil (X ∩ y) | **2 clientes** |

➡️ Ou seja, apenas **2 amostras completas** estavam disponíveis para treino — inviabilizando uma modelagem estatisticamente significativa.

### 🧭 Estratégia adotada

Diante disso, a decisão foi **não comprometer o rigor metodológico tentando forçar resultados numéricos**, mas sim **entregar uma Prova de Conceito (PoC)** funcional e bem estruturada:

  - Modelo: `MultiOutputClassifier(LogisticRegression())`
  - Vetorizador: `TfidfVectorizer()`
  - Objetivo: Demonstrar **a arquitetura do pipeline**, geração de artefatos (`model.joblib` e `vectorizer.joblib`) e funcionamento completo da **API Flask**.

-----

## 🚀 Execução e Teste da API

A API foi desenvolvida com **Flask**, consumindo os artefatos treinados e expondo endpoints REST.

### 1\. 🧩 Pré-requisitos

  - Python 3.x
  - Git

### 2\. ⚙️ Configuração do ambiente

```bash
# Clone o repositório
git clone https://github.com/seuusuario/desafio-agile.git
cd desafio-agile

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate    # Linux/Mac
# .\venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 3\. ▶️ Rodando a API

```bash
# Inicie o servidor Flask
python api.py
```

O terminal exibirá:

```
* Running on http://127.0.0.1:5000/
```

### 4\. 🔎 Testando os Endpoints

| Tipo de Teste | URL | Descrição |
| :--- | :--- | :--- |
| ✅ **Home** | [http://127.0.0.1:5000/](http://127.0.0.1:5000/) | Página inicial da API |
| ✅ **Cliente 2** | [http://127.0.0.1:5000/predict/2](http://127.0.0.1:5000/predict/2) | Cliente presente no treino |
| ✅ **Cliente 3** | [http://127.0.0.1:5000/predict/3](http://127.0.0.1:5000/predict/3) | Cliente fora do treino |
| ❌ **Cliente 999** | [http://127.0.0.1:5000/predict/999](http://127.0.0.1:5000/predict/999) | Cliente inexistente (erro 404) |

-----

## 🗂️ Estrutura do Repositório

```
desafio-agile
├─ README.md
│   → Documento principal do projeto, descreve objetivos, instalação, uso e estrutura geral.
│
├─ api.py
│   → Script da API desenvolvida em Flask.
│     Responsável por carregar o modelo treinado e servir previsões via requisições HTTP.
│
├─ requirements.txt
│   → Lista de dependências Python necessárias para executar o projeto (Flask, joblib, pandas, etc).
│
├─ artifacts
│   → Diretório com artefatos do modelo de Machine Learning.
│     ├─ model.joblib             → Modelo final treinado e serializado.
│     └─ vectorizer.joblib        → Vetorizador usado no pré-processamento de texto.
│
├─ data
│   → Contém os dados utilizados no desenvolvimento e teste do projeto.
│     ├─ chat_history.csv         → Histórico de mensagens e interações do cliente.
│     ├─ client.csv               → Informações cadastrais dos clientes.
│     ├─ client_conditions.csv    → Condições de saúde associadas a cada cliente.
│     ├─ seed_ciap_chapters.csv   → Dados seed referentes aos capítulos do CIAP.
│     ├─ seed_ciap_components.csv → Dados seed referentes aos componentes do CIAP.
│     └─ seed_ciap_raw.csv        → Dados brutos originais do CIAP.
│
├─ notebooks
│   → Contém notebooks Jupyter usados na exploração e modelagem dos dados.
│     └─ Projeto_Agile.ipynb      → Notebook principal de EDA (análise exploratória),
│                                   pré-processamento, treinamento e avaliação do modelo.
```

-----

## 🧩 Principais Aprendizados e Destaques Técnicos

  - 🧠 **Capacidade de análise sob limitação de dados** — foco na solução e não na frustração.
  - 🏗️ **Pipeline modular e reprodutível**, pronto para ser expandido com novos dados.
  - 🔍 **NLP aplicado a contexto real de linguagem clínica**.
  - 🧰 **Entrega funcional de ponta a ponta:** dados → modelo → artefatos → API.
  - 🚀 **Clean code e documentação completa**, facilitando auditoria e evolução do projeto.

-----

## 🔮 Melhorias Futuras e Visão de Longo Prazo

O *pipeline* atual foi construído como uma Prova de Conceito robusta. Dada a limitação de dados de treino (N=2), o próximo passo lógico seria evoluir a solução nas seguintes frentes:

1.  **Ingestão de Dados:** O primeiro passo seria obter um conjunto de dados de treino maior e mais representativo para permitir uma modelagem estatística real.
2.  **Modelagem NLP Avançada:** Substituir o *baseline* (TF-IDF + Regressão Logística) por modelos de linguagem baseados em Transformers (ex: **BERTimbau**). Esses modelos entendem o contexto, a semântica e as negações (ex: "eu *não* tenho diabetes" vs. "eu tenho diabetes"), o que aumentaria drasticamente a acurácia.
3.  **Modelo Multimodal:** Utilizar os metadados dos clientes (`idade`, `genero`, `cidade`) que foram descartados neste *baseline*. Um modelo mais avançado poderia combinar as *features* de texto (do BERT) com as *features* tabulares, criando um sistema de recomendação mais completo.
4.  **Extração de Informação (IE) e *Weak Supervision*:** Usar os arquivos `seed_*.csv` (com critérios de inclusão e exclusão) não apenas como dicionários, mas como base para um sistema de *Weak Supervision*. Poderíamos criar regras (ex: regex, spaCy) para identificar menções a "glicose alta" ou "fumo" e usá-las para rotular automaticamente milhares de chats, criando um conjunto de treino maior sem esforço manual.
