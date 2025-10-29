import pandas as pd
import joblib
from flask import Flask, jsonify, request

# --- 1. Carregamento de Artefatos e Dados ---
print("Carregando artefatos e dados...")

# Caminhos de arquivo (agora estão organizados)
PATH_MODEL = "artifacts/model.joblib"
PATH_VECTORIZER = "artifacts/vectorizer.joblib"
PATH_CLIENTS_DATA = "data/client.csv"
PATH_CHAT_DATA = "data/chat_history.csv"

# Carrega os modelos salvos
try:
    vectorizer = joblib.load(PATH_VECTORIZER)
    model = joblib.load(PATH_MODEL)
    print("Modelos carregados com sucesso.")
except FileNotFoundError:
    print("ERRO: 'vectorizer.joblib' ou 'model.joblib' não encontrados na pasta 'artifacts/'.")
    exit()

# Carrega os dados brutos necessários para a API
try:
    df_clientes = pd.read_csv(PATH_CLIENTS_DATA)
    df_chat = pd.read_csv(PATH_CHAT_DATA)
    # Converte a data (essencial para a ordenação)
    df_chat['created_date_brt'] = pd.to_datetime(df_chat['created_date_brt'])
    print("Dados brutos (CSVs) carregados com sucesso.")
except FileNotFoundError:
    print(f"ERRO: Arquivos CSV não encontrados na pasta 'data/'.")
    exit()

# --- 2. Definições e Funções Auxiliares ---

# A mesma função de formatação do Colab
def formatar_conversa(df_grupo):
    senders_str = df_grupo['sender'].fillna('')
    messages_str = df_grupo['message_text'].fillna('')
    mensagens_formatadas = senders_str + ": " + messages_str
    return " \n ".join(mensagens_formatadas)

# Nomes das colunas alvo (do seu treino)
target_names = ['e66', 'g47', 'i82', 'k57']

# Mapeamento (do seed_raw) para uma resposta amigável
cid_map = {
    'e66': 'Obesidade',
    'g47': 'Distúrbios do Sono',
    'i82': 'Embolia/Trombose Venosa',
    'k57': 'Doença Diverticular'
}
print("Funções auxiliares e mapeamento CID prontos.")

# --- 3. Criação da Aplicação Flask ---

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>API do Desafio Técnico</h1><p>Use o endpoint /predict/&lt;client_id&gt; para testar.</p>"

# --- 4. O Endpoint de Predição ---

@app.route("/predict/<int:client_id>", methods=['GET'])
def predict(client_id):
    
    print(f"\n[API] Recebida requisição para client_id: {client_id}")
    
    # --- 404 Check ---
    client_info = df_clientes[df_clientes['client_id'] == client_id]
    
    if client_info.empty:
        print(f"[API] ERRO: client_id {client_id} não encontrado (404).")
        return jsonify({"erro": "Cliente não encontrado (404 Not Found)"}), 404
    
    # --- Buscar os dados do cliente ---
    try:
        chat_id_key = client_info.iloc[0]['chat_message_id']
        historico_chat = df_chat[df_chat['chat_channel_id'] == chat_id_key]
        
        if historico_chat.empty:
            print(f"[API] Sucesso: client_id {client_id} encontrado, mas não possui chats.")
            return jsonify({
                "client_id": client_id,
                "condicoes_previstas": []
            })

        # --- Pré-processamento (Igual ao Treino) ---
        historico_chat = historico_chat.sort_values(by='created_date_brt')
        texto_completo = formatar_conversa(historico_chat)
        
        texto_para_vetorizar = [texto_completo]
        
        # --- Predição ---
        X_vetorizado = vectorizer.transform(texto_para_vetorizar)
        predicao_binaria = model.predict(X_vetorizado)
        
        # --- Formatar a Resposta ---
        condicoes_encontradas = []
        for i, nome_alvo in enumerate(target_names):
            if predicao_binaria[0][i] == 1:
                nome_doenca = cid_map.get(nome_alvo, nome_alvo)
                condicoes_encontradas.append(nome_doenca)
        
        print(f"[API] Sucesso: client_id {client_id}. Condições: {condicoes_encontradas}")
        return jsonify({
            "client_id": int(client_id),
            "condicoes_previstas": condicoes_encontradas
        })

    except Exception as e:
        print(f"[API] ERRO 500: {str(e)}")
        return jsonify({"erro": "Erro interno no servidor", "detalhe": str(e)}), 500

# --- 5. Rodar a Aplicação (Apenas se executado como script) ---
if __name__ == "__main__":
    # porta 5000 é o padrão do Flask
    app.run(debug=True, port=5000)
