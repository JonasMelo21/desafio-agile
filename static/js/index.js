const button = document.getElementById('search_button');
const input = document.getElementById('client_id_input');
const resultsDiv = document.getElementById('results');


button.addEventListener('click', async () => {
    const clientId = input.value;

    // 1. Limpa resultados e verifica se há um ID
    resultsDiv.innerHTML = 'Buscando...';
    if (!clientId) {
        resultsDiv.innerHTML = '<p class="error">Por favor, insira um ID.</p>';
        return;
    }

    try {
        // 2. Chama a nossa própria API Flask
        const response = await fetch(`/predict/${clientId}`);
        const data = await response.json();

        // 3. Mostra os resultados na tela
        if (response.status === 404) {
            // Erro 404 (Cliente não encontrado)
            resultsDiv.innerHTML = `<p class="error"><b>Erro 404:</b> ${data.erro}</p>`;
        } else if (!response.ok) {
            // Outros erros
            throw new Error(data.erro || 'Erro desconhecido');
        } else {
            // Sucesso!
            const conditions = data.condicoes_previstas;
            if (conditions.length > 0) {
                const items = conditions.map(item => `<li>${item}</li>`).join('');
                resultsDiv.innerHTML = `
                            <p class="success"><b>Condições previstas para o Cliente ${data.client_id}:</b></p>
                            <ul>${items}</ul>
                        `;
            } else {
                resultsDiv.innerHTML = `<p>Nenhuma condição prevista encontrada para o Cliente ${data.client_id}.</p>`;
            }
        }

    } catch (err) {
        resultsDiv.innerHTML = `<p class="error"><b>Erro na requisição:</b> ${err.message}</p>`;
    }
});