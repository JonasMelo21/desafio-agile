Aqui está o `README.md` refinado, com as seções duplicadas consolidadas e todos os traços de IA e linhas horizontais removidos, pronto para o seu repositório.

-----

# 🧠 Desafio Técnico — API de Classificação de Saúde

Este repositório contém a solução completa para um **desafio técnico de Machine Learning**.
O objetivo foi **construir um pipeline funcional de ponta a ponta**, capaz de ler, processar e interpretar históricos de chat clínico para **identificar condições de saúde** dos clientes — tudo integrado a uma **API Flask pronta para consumo.**

## 🎯 O Desafio

O objetivo foi desenvolver um modelo de NLP para classificar condições de saúde (Obesidade, Diabetes, etc.) com base em históricos de chat. A entrega é uma **API Flask** que recebe um `client_id`, retorna uma lista de condições previstas e trata o erro `404 Not Found`.

Conforme a expectativa do desafio, o foco principal foi **demonstrar um processo claro de investigação**, tomada de decisão e a construção de um pipeline *end-to-end* funcional.

## 💡 Abordagem e Metodologia

Desenvolvi o projeto seguindo uma **linha lógica de investigação e prototipagem rápida**, priorizando clareza e reprodutibilidade.

### 1\. 🔍 Exploração e Pré-Processamento (EDA)

  * **Análise de relacionamentos** entre os CSVs (`client`, `chat_history`, `client_conditions`, `seed_*`), mapeando chaves e integridades.
  * **Identificação do alvo (`y`)**: o arquivo `client_conditions.csv` foi definido como rótulo do modelo.
  * **Entendimento dos dicionários (`seed_*`)**: interpretados como tabelas de referência, úteis para enriquecer e validar as condições de saúde.

### 2\. 🧱 Engenharia de Features (Preparação do X)

  * Para preservar o contexto do diálogo, as mensagens foram **ordenadas por data** e **prefixadas** com o remetente (`client:` ou `user:`).
  * Todas as mensagens de um cliente foram **concatenadas** em um único documento textual — resultando em uma representação contextualizada e sem ruído.
  * Esse texto passou por **vetorização com TF-IDF**, otimizando a entrada para o modelo.

### 3\. 🎯 Preparação do Alvo (Preparação do y)

  * O dataset de condições foi convertido de formato *longo* para *wide*, via `pandas.crosstab`, gerando um **DataFrame multi-rótulo** (cada coluna = uma condição binária).
  * Exemplo:
    ```
    client_id | e66 | g47 | z72
         1    |  1  |  0  |  1
    ```

### 4\. 🤖 Modelagem Baseline

  * Para criar uma Prova de Conceito (PoC) robusta, utilizei um pipeline clássico de NLP:
      * **Features:** `TfidfVectorizer` para extrair features do texto.
      * **Modelo:** `MultiOutputClassifier(LogisticRegression())` para lidar com a classificação multi-rótulo.

## ⚠️ Insight Principal: A Limitação de Dados

A investigação (o foco do desafio) revelou uma limitação crítica:

| Tipo de Dado | Nº de Clientes Únicos |
| :--- | :---: |
| Histórico de Chat (`X`) | 3 |
| Condições Rotuladas (`y`) | 2 |
| **Amostras Treináveis (X ∩ y)** | **2** |

Com apenas 2 amostras de treino, a decisão foi **não focar em métricas de acurácia**, mas sim em **provar a arquitetura do pipeline**. Os artefatos (`model.joblib`, `vectorizer.joblib`) foram gerados para demonstrar que a API funciona de ponta-a-ponta.

## 🚀 Como Testar a API (Localmente)

A API possui um frontend simples para testes interativos.

```bash
# 1. Clone o repositório e entre na pasta
git clone https://github.com/JonasMelo21/desafio-agile.git
cd desafio-agile

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate    # Linux/Mac (ou .\venv\Scripts\activate no Windows)

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a API
python api.py
```

Após rodar, acesse **`http://127.0.0.1:5000/`** no seu navegador para usar a interface de teste.

**IDs para teste:**

  * `2` (Cliente presente no treino)
  * `3` (Cliente novo, fora do treino)
  * `999` (Cliente inexistente, retornará 404)

## 🧩 Destaques e Aprendizados

  * 🧠 **Capacidade de análise sob limitação de dados**, com foco na entrega de uma PoC funcional e não na frustração pela falta de dados.
  * 🏗️ **Pipeline NLP *end-to-end*** (Dados → Modelo → API) modular e reprodutível, pronto para ser expandido com novos dados.
  * 🔍 **NLP aplicado a contexto real** de linguagem clínica.
  * 🧰 **Entrega de valor agregado** com um frontend simples para testes e validação.
  * 🚀 **Clean code e documentação clara**, facilitando auditoria e evolução do projeto.

## 🔮 Próximos Passos e Melhorias Futuras

O *pipeline* atual foi construído como uma Prova de Conceito robusta. Os próximos passos lógicos seriam:

1.  **Ingestão de Dados:** O primeiro passo seria obter um conjunto de dados de treino maior e mais representativo para permitir uma modelagem estatística real.
2.  **Modelagem NLP Avançada:** Substituir o *baseline* (TF-IDF + Regressão Logística) por modelos de linguagem baseados em Transformers (ex: **BERTimbau**). Esses modelos entendem o contexto, a semântica e as negações (ex: "eu *não* tenho diabetes" vs. "eu tenho diabetes"), o que aumentaria drasticamente a acurácia.
3.  **Modelo Multimodal:** Utilizar os metadados dos clientes (`idade`, `genero`, `cidade`) que foram descartados neste *baseline*. Um modelo mais avançado poderia combinar as *features* de texto (do BERT) com as *features* tabulares, criando um sistema de classificação mais completo.
4.  **Extração de Informação (IE) e *Weak Supervision*:** Usar os arquivos `seed_*.csv` (com critérios de inclusão e exclusão) não apenas como dicionários, mas como base para um sistema de *Weak Supervision*. Poderíamos criar regras (ex: regex, spaCy) para identificar menções a "glicose alta" ou "fumo" e usá-las para rotular automaticamente milhares de chats, criando um conjunto de treino maior sem esforço manual.
