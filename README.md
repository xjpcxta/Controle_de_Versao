# Controle Financeiro Pessoal

## Descrição do Projeto

Este projeto consiste em uma aplicação web para gerenciamento de gastos pessoais, desenvolvida como avaliação da disciplina de Qualidade de Software. O sistema permite que os usuários se cadastrem, autentiquem e realizem o controle de suas finanças de maneira simples e intuitiva, registrando e categorizando suas despesas. O principal objetivo foi aplicar na prática os conceitos de controle de versão com Git e GitHub, metodologias ágeis e as boas práticas de qualidade de software baseadas na norma ISO/IEC 25010.

## Tecnologias Utilizadas

- **Backend:** Python 3
- **Framework Web:** Flask
- **Frontend:** HTML5 e CSS3
- **Banco de Dados:** SQLite (implícito pelo arquivo `gastos.db`)
- **Controle de Versão:** Git & GitHub

## Instruções de Instalação e Execução

Para executar este projeto localmente, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/xjpcxta/Controle_de_Versao.git](https://github.com/xjpcxta/Controle_de_Versao.git)
    cd Controle_de_Versao
    ```

2.  **Crie e ative um ambiente virtual (Opcional, mas recomendado):**
    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências do projeto:**
    *(Nota: Crie um arquivo `requirements.txt` com o comando `pip freeze > requirements.txt` e adicione as bibliotecas usadas, como o Flask e Werkzeug).*
    ```bash
    pip install Flask werkzeug
    ```

4.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

5.  Acesse `http://127.0.0.1:5000` no seu navegador.

## Funcionalidades Implementadas

A aplicação conta com as seguintes funcionalidades:

-   [x] **Gerenciamento de Usuários:** Sistema completo de registro e login de usuários.
-   [x] **Adicionar Gasto:** Permite ao usuário registrar uma nova despesa.
-   [x] **Editar Gasto:** Oferece a opção de modificar informações de um gasto já registrado.
-   [x] **Excluir Gasto:** Possibilita a remoção de um gasto da lista.
-   [x] **Categorização de Gastos:**
    -   Marcar despesas como **Recorrentes**.
    -   Marcar despesas como **Irrelevantes**.

## Características de Qualidade Aplicadas (ISO/IEC 25010)

Durante o desenvolvimento, foram priorizadas as seguintes características de qualidade de software:

1.  **Funcionalidade:** O sistema atende a todos os requisitos funcionais especificados, garantindo que as operações de CRUD (Criar, Ler, Atualizar, Excluir) em despesas e o gerenciamento de usuários operem corretamente.
2.  **Confiabilidade:** Foram implementadas validações nos formulários e tratamento de erros para assegurar que a aplicação se mantenha estável e evite falhas inesperadas durante o uso.
3.  **Usabilidade:** A interface foi projetada para ser clara e intuitiva, permitindo que o usuário realize as tarefas de forma fácil e com o mínimo de esforço.
4.  **Manutenibilidade:** O código foi estruturado de forma modular e com nomes claros para variáveis e funções, facilitando futuras manutenções, correções ou implementações de novas funcionalidades.
5.  **Portabilidade:** O uso de tecnologias padrão (Python, Flask) e a documentação do processo de instalação garantem que a aplicação possa ser executada em diferentes ambientes de forma consistente.

## Integrante

-   **Nome:** João Pedro da Costa Porto Gonçalves
-   **Matrícula:** UC24201429
-   **Função:** Desenvolvedor Full-Stack
