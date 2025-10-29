Desafio Técnico: API de Classificação de Saúde
Este repositório contém a solução para um desafio técnico de Machine Learning focado em NLP (Processamento de Linguagem Natural). O objetivo é construir um pipeline completo, desde a análise de dados até uma API funcional.

🎯 O Desafio
O desafio consistia em desenvolver um modelo de Machine Learning capaz de identificar condições de saúde de clientes (ex: Obesidade, Diabetes, Tabagismo) com base em seus históricos de chat.

A entrega final deveria ser uma API que:

Recebesse um client_id como parâmetro.

Retornasse uma lista com as condições de saúde previstas para esse cliente.

Retornasse um erro 404 Not Found caso o cliente não existisse.

O foco principal era avaliar o processo de investigação e as tomadas de decisão.

💡 Abordagem e Pipeline de Dados
O projeto foi estruturado seguindo um pipeline de ML padrão, desde a exploração até a implantação de uma Prova de Conceito (PoC).

1. Exploração e Pré-processamento (EDA)
Análise de Chaves: Foi feita a análise de todos os CSVs para entender o esquema e as relações. As chaves client_id, chat_message_id (nos clientes) e chat_channel_id (nos chats) foram mapeadas.

Análise do Alvo (y): O client_conditions.csv foi identificado como o "gabarito" (alvo) do modelo.

Análise dos Dicionários: Os arquivos seed_*.csv foram identificados como tabelas de mapeamento (ex: cid10 para nomes de doenças).

2. Engenharia de Features (Preparação do X)
A simples concatenação de mensagens misturaria as falas do paciente e do profissional. Para dar contexto ao modelo, o histórico de chat foi transformado em um "roteiro" formatado:

As mensagens foram ordenadas por data (created_date_brt).

Um prefixo (client: ou user: ) foi adicionado a cada mensagem com base na coluna sender.

Todas as mensagens de um mesmo cliente foram agrupadas em um único documento de texto.

3. Preparação do Alvo (Preparação do y)
Para o modelo de classificação multi-rótulo, o df_client_conditions (que estava em formato "longo") foi "pivotado" usando pd.crosstab. Isso resultou em um DataFrame onde cada cliente tinha uma linha e cada condição (e66, g47, etc.) era uma coluna binária (0 ou 1).

⚠️ Principal Insight e Tomada de Decisão
A etapa de investigação (o foco do desafio) revelou uma limitação crítica nos dados de treino.

Ao cruzar os dados, descobrimos que:

Clientes com histórico de chat (df_X): 3

Clientes com "gabarito" (rótulos de condição df_y): 2

Resultado: A interseção (dados treináveis) continha apenas 2 amostras.

Tomada de Decisão Estratégica
Sendo estatisticamente inviável treinar um modelo preditivo real ou realizar uma divisão treino/teste com 2 amostras, o foco foi alterado para provar a funcionalidade do pipeline de ponta-a-ponta (Proof of Concept).

Um pipeline de TfidfVectorizer + MultiOutputClassifier(LogisticRegression()) foi treinado nessas 2 amostras. O objetivo não foi a acurácia, mas sim a criação dos artefatos (vectorizer.joblib e model.joblib) para demonstrar que a API é capaz de carregar, pré-processar dados novos e consumir um modelo treinado.

🚀 Como Executar e Testar a API
O projeto inclui uma API Flask (api.py) que consome os artefatos de modelo treinados.

1. Pré-requisitos
Python 3.x

Git

2. Configuração do Ambiente
(Assumindo que o repositório já foi clonado)

Bash

# 1. Crie um ambiente virtual
python -m venv venv

# 2. Ative o ambiente
# (No Linux/Mac)
source venv/bin/activate
# (No Windows)
# .\venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
3. Rodando a API
Bash

# 4. Inicie o servidor Flask
python api.py
O terminal indicará que o servidor está rodando em http://127.0.0.1:5000/.

4. Testando os Endpoints
Abra seu navegador ou use uma ferramenta como curl para testar os endpoints:

Rota Raiz (Home): http://127.0.0.1:5000/

Teste (Cliente 2 - Estava no treino): http://127.0.0.1:5000/predict/2

Teste (Cliente 3 - Não estava no treino): http://127.0.0.1:5000/predict/3

Teste (Cliente 404 - Não Encontrado): http://127.0.0.1:5000/predict/999

📂 Estrutura do Repositório
/desafio-agile
|
|-- README.md               # Este arquivo
|-- api.py                  # O script da API Flask
|-- requirements.txt        # Dependências do Python
|
|-- artifacts/              # Modelos treinados e serializados
|   |-- model.joblib
|   |-- vectorizer.joblib
|
|-- data/                   # Dados brutos fornecidos no desafio
|   |-- chat_history.csv
|   |-- client.csv
|   |-- client_conditions.csv
|   |-- seed_*.csv
|
|-- notebooks/              # Notebook de exploração e treinamento (EDA)
|   |-- Projeto_Agile.ipynb
|
|-- docs/                   # Documentação original dos dados
|   |-- data_readme.md
|   |-- data_readme.pdf
|
|-- venv/                   # (Ignorado pelo Git)