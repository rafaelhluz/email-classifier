# 📧 Classificador de E-mails com IA

> Uma solução de Inteligência Artificial para classificar e-mails de clientes como "Produtivos" ou "Improdutivos" e gerar respostas inteligentes e contextualizadas.

---

### Funcionalidades

- **Classificação de E-mails:** Categoriza e-mails como "Produtivos" ou "Improdutivos" usando um modelo de IA.
- **Respostas Inteligentes:** Gera respostas sugeridas e contextualizadas para e-mails "Produtivos".
- **Respostas Padrão:** Fornece respostas de fallback para e-mails "Improdutivos", otimizando o fluxo de trabalho.
- **Interface Web Intuitiva:** Uma interface simples e amigável para colar o conteúdo dos e-mails e obter o resultado da classificação.

---

### Tecnologias Utilizadas

- **Backend:**
    - [FastAPI](https://fastapi.tiangolo.com/pt/): Framework web para criação da API.
    - [Uvicorn](https://www.uvicorn.org/): Servidor web ASGI para rodar a aplicação FastAPI.
    - [Google Generative AI SDK](https://github.com/google/generative-ai-python): Biblioteca para interagir com o modelo de IA.
- **Frontend:**
    - [HTML/CSS](https://developer.mozilla.org/pt-BR/docs/Web/HTML): Estrutura e estilo da interface.
    - [Jinja2](https://pypi.org/project/Jinja2/): Motor de template para renderizar a página web.
- **Deploy:**
    - [Vercel](https://vercel.com/): Plataforma de hospedagem para deploy da aplicação.

---

### Como Rodar o Projeto Localmente

Para testar o projeto na sua máquina, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/rafaelhluz/email-classifier.git](https://github.com/rafaelhluz/email-classifier.git)
    cd seu-repositorio
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1   # No Windows PowerShell
    # ou
    source venv/bin/activate      # No Linux/macOS
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure a chave de API:**
    - Crie um arquivo chamado `.env` na raiz do projeto.
    - Adicione sua chave de API do Google Gemini:
    ```
    GEMINI_API_KEY="sua_chave_de-api-aqui"
    ```
5.  **Inicie a aplicação:**
    ```bash
    uvicorn app.main:app --reload
    ```
    A aplicação estará disponível em `http://127.0.0.1:8000`.

---

### Link de Deploy

A aplicação está hospedada na Vercel e pode ser acessada através do link:

[Link da sua aplicação na Vercel](https://email-classifier-nine.vercel.app/)

---

### 👨Autor

- **[Rafael Henrique da Luz](https://github.com/rafaelhluz)**

---

### Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.