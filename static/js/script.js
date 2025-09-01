document.getElementById('emailForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.querySelector('#file');
    const textInput = document.querySelector('#email_text');
    const loading = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    
    if (!fileInput.files[0] && !textInput.value.trim()) {
        alert('Por favor, insira texto ou selecione um arquivo.');
        return;
    }

    resultDiv.classList.remove('show');
    resultDiv.style.display = 'none';
    loading.style.display = 'block';

    if (fileInput.files[0]) {
        formData.append('file', fileInput.files[0]);
    } else {
        formData.append('email_text', textInput.value);
    }

    try {
        const response = await fetch('/classify', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        if (response.ok) {
            resultDiv.className = `result ${result.category === 'Produtivo' ? 'productive' : 'unproductive'}`;
            resultDiv.innerHTML = `
                <h3>Classificação: ${result.category}</h3>
                <p><strong>Resposta sugerida:</strong></p>
                <p style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 5px; border-left: 4px solid currentColor;">
                    ${result.response}
                </p>
                <p><strong>Caracteres processados:</strong> ${result.characters_processed}</p>
                <p><strong>Preview:</strong> ${result.email_text.substring(0, 150)}${result.email_text.length > 150 ? '...' : ''}</p>
            `;

            textInput.value = '';
            fileInput.value = '';

            resultDiv.style.display = 'block';
            setTimeout(() => resultDiv.classList.add('show'), 50);
        } else {
            alert('Erro: ' + (result.error || 'Erro desconhecido'));
        }
    } catch (error) {
        alert('Erro de conexão: ' + error.message);
    } finally {
        loading.style.display = 'none';
    }
});
