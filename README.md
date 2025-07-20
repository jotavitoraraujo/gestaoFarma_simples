# 薬 GestãoFarma Simples — Sistema de Gestão para Farmácias

Este projeto tem como objetivo desenvolver um sistema de gestão de estoque e financeiro em Python, com foco total em simplicidade e eficiência. A solução é desenhada para atender às necessidades de pequenas farmácias de bairro, onde os processos ainda são, em grande parte, manuais e ineficientes, visando um público-alvo não técnico.

---

## ⚙️ Funcionalidades Atuais

-   ✅ **Arquitetura Orientada a Objetos (POO):** O projeto foi arquitetado usando Classes (`Produto`, `Lote`, `Usuario`), tornando o código organizado, reutilizável e alinhado com as melhores práticas de engenharia.
-   ✅ **Modelo de Dados Relacional:** Implementado um schema robusto com tabelas separadas para `produtos`, `lotes` e `usuarios`, garantindo a integridade dos dados.
-   ✅ **Automação de Entrada de Estoque:** O sistema realiza o fluxo completo de importação de NF-e, criando e manipulando objetos `Produto` e `Lote`.
-   ✅ **Gestão de Usuários Segura:** Implementada a funcionalidade de cadastro de vendedores, com validação de entradas e armazenamento seguro do PIN usando o algoritmo de hash SHA-256.
-   ✅ **Entrada de Senha Mascarada:** A interface de terminal utiliza a biblioteca `pwinput` para mascarar a digitação do PIN com asteriscos, garantindo a privacidade e segurança do usuário.
-   ➡️ **Próxima Fase (Login e Vendas):** O próximo passo é construir a tela de login e a funcionalidade de "Registrar Venda".

---

## 🧱 Tecnologias Utilizadas

-   **Python 3.12+**
-   **VS Code**

### Bibliotecas Externas:

-   `pwinput` - Para entrada segura e mascarada de senhas no terminal.

### Bibliotecas Padrão:

-   `sqlite3` (Banco de Dados)
-   `xml.etree.ElementTree` (Leitura de XML)
-   `datetime` (Manipulação de Datas)
-   `hashlib` (Criptografia de Hash)
-   `os`, `pathlib`

*O projeto utiliza poucas dependências externas para garantir leveza e portabilidade, permitindo que rode em computadores mais antigos sem a necessidade de uma instalação complexa.*

---

## 🚀 Como Executar

1.  Clone o projeto:
    ```bash
    git clone [https://github.com/jotavitoraraujo/gestaoFarma_simples.git](https://github.com/jotavitoraraujo/gestaoFarma_simples.git)
    cd gestaoFarma_simples
    ```
2.  Crie e ative o ambiente virtual:
    ```bash
    py -m venv venv
    venv\Scripts\activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute o projeto:
    ```bash
    py main.py
    ```

---

## 🧩 Estrutura do Projeto

```
gestaoFarma_simples/
├── dados/
│   └── farmacia.db
│
├── sistema/
│   ├── __init__.py
│   ├── database.py
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── produto.py
│   │   └── lote.py
│   └── modulos/
│       ├── __init__.py
│       ├── importador_nfe.py
│       ├── relatorios.py
│       ├── users.py
│       └── validadores_input.py
│
├── .gitignore
├── LICENSE
├── README.md
├── main.py
└── requirements.txt
```

---

## 👨‍💻 Autor

Desenvolvido por **João Vitor Araújo** — Estudante de Análise e Desenvolvimento de Sistemas.

Venho de uma linhagem de construtores. Meu avô, Franco, era pedreiro; meu pai, Frankly, o arquiteto e construtor de projetos complexos. Eles construíam com as mãos. Descobri que minha forma de construir é com código.

Este projeto nasceu dessa percepção. Após desenvolver um agente autônomo para análise de dados on-chain (`want33d`), voltei meu olhar para problemas do mundo real e identifiquei uma necessidade no negócio do meu pai. O GestãoFarma Simples é a aplicação da tecnologia com empatia, para resolver uma dor real com uma solução robusta, mas de simples utilização.

-   [LinkedIn](https://www.linkedin.com/in/joaoaraujo-dev/)
-   [GitHub](https://github.com/jotavitoraraujo)

---

## 📅 Histórico de Atualizações

-   **02/07/2025 — Fase 0 (Fundação):** Criação do repositório e da estrutura inicial do projeto.
-   **11/07/2025 — Fase 1 (Arquitetura de Dados):** Refatoração do banco de dados para um modelo relacional (`produtos` + `lotes`).
-   **13/07/2025 — Fase 2 (Início - Gestão de Usuários):** Criação da tabela `usuarios` e implementação do cadastro de vendedor com hashing de PIN.
-   **16/07/2025 — Fase 2 (Refatoração para POO):** Decisão arquitetônica e refatoração do sistema para Programação Orientada a Objetos, com a criação das classes `Produto` e `Lote` e a modularização da lógica de importação e validação.
-   **20/07/2025 — Fase 2 (Refatoração para POO - Parte 2):** Conclusão da refatoração para POO nos módulos de banco de dados e importação" -m "- Funções em `database.py` (buscar_produto, produtos_existentes) foram atualizadas para operar com objetos Produto. A lógica de importação foi extraída do `main.py` para o novo módulo `importador_nfe.py` e refatorada para usar a nova arquitetura de objetos."

---

## 📌 Observações Finais

O **GestãoFarma Simples** foi desenvolvido com o usuário final em mente: pessoas não técnicas que precisam de uma ferramenta que funcione de forma direta e sem complicações. A filosofia do projeto é priorizar a simplicidade na interface e a robustez na lógica de automação, resolvendo uma dor real do pequeno comerciante com tecnologia acessível.

A arquitetura de dados e de software está sendo desenhada para espelhar as melhores práticas da indústria, garantindo não apenas a simplicidade, mas também a precisão, a segurança e a integridade das informações do negócio a longo prazo.