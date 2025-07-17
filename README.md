# 薬 GestãoFarma Simples — Sistema de Gestão para Farmácias

Este projeto tem como objetivo desenvolver um sistema de gestão de estoque e financeiro em Python, com foco total em simplicidade e eficiência. A solução é desenhada para atender às necessidades de pequenas farmácias de bairro, onde os processos ainda são, em grande parte, manuais e ineficientes, visando um público-alvo não técnico.

---

## ⚙️ Funcionalidades Atuais

-   ✅ **Arquitetura de Dados Relacional:** Implementado um schema robusto com tabelas separadas para `produtos` e `lotes`, garantindo a integridade dos dados para um controle de estoque preciso.
-   ✅ **Automação de Entrada de Estoque:** O sistema realiza o fluxo completo de importação de NF-e, incluindo leitura do XML, identificação de produtos novos vs. existentes, e a inserção/atualização dos dados no banco.
-   ✅ **Validação de Entrada Robusta:** A interface de cadastro de novos itens valida os dados de preço e data de validade para garantir a consistência e segurança das informações.
-   ✅ **Cadastro de Usuários com Hashing de PIN:** Implementada a funcionalidade inicial de cadastro de vendedores, com validação de entradas e armazenamento seguro do PIN usando o algoritmo de hash SHA-256.
-   ✅ **Controle de Versão Profissional:** O projeto está totalmente configurado e mantido com Git e GitHub, seguindo boas práticas de commits.
-   ➡️ **Próxima Fase (Login e Vendas):** O próximo passo é construir a tela de login para os usuários cadastrados e, em seguida, a funcionalidade de "Registrar Venda".

---

## 🧱 Tecnologias Utilizadas

-   **Python 3.12+**
-   **VS Code**

### Bibliotecas Padrão:

-   `sqlite3` (Banco de Dados)
-   `xml.etree.ElementTree` (Leitura de XML)
-   `datetime` (Manipulação de Datas)
-   `hashlib` (Criptografia de Hash)
-   `os`, `pathlib`

*O projeto foi intencionalmente desenvolvido com o mínimo de dependências externas para garantir leveza e portabilidade, permitindo que rode em computadores mais antigos sem a necessidade de uma instalação complexa.*

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
3.  Execute o projeto:
    ```bash
    py main.py
    ```

---

## 🧩 Estrutura do Projeto

```
gestaoFarma_simples/
├── dados/
│   ├── farmacia.db
│   └── exemplo_nfe.xml
│
├── sistema/
│   ├── __init__.py
│   ├── database.py
│   └── modulos/
│       ├── __init__.py
│       ├── leitor_xml.py
│       └── users.py
│
├── .gitignore
├── LICENSE
├── main.py
└── README.md
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
-   **11/07/2025 — Fase 1 (Arquitetura e Entrada de Dados):** Refatoração completa do banco de dados para um modelo relacional (`produtos` + `lotes`) e implementação do fluxo de importação de NF-e com validação de dados.
-   **13/07/2025 — Fase 2 (Início - Gestão de Usuários):** Criação da tabela `usuarios` e implementação da funcionalidade de cadastro de vendedor com validação de entradas e hashing de PIN (SHA-256).
-   **16/07/2025 — Fase 2 (Refatoração para POO):** Decisão arquitetônica de migrar para Programação Orientada a Objetos. Implementação das classes `Produto` e `Lote` e refatoração do `leitorXML` para operar com objetos.

---

## 📌 Observações Finais

O **GestãoFarma Simples** foi desenvolvido com o usuário final em mente: pessoas não técnicas que precisam de uma ferramenta que funcione de forma direta e sem complicações. A filosofia do projeto é priorizar a simplicidade na interface e a robustez na lógica de automação, resolvendo uma dor real do pequeno comerciante com tecnologia acessível.

A arquitetura de dados e de segurança está sendo desenhada para espelhar as melhores práticas da indústria, garantindo não apenas a simplicidade, mas também a precisão e a integridade das informações do negócio a longo prazo.