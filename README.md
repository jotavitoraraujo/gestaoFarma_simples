# 薬 GestãoFarma Simples — Sistema de Gestão para Farmácias

<p align="center">
  <img src="./assets/gestaofarma_simples_logo_v2.png" alt="Logo do GestãoFarma Simples" width="200"/>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Tested%20with-Pytest-green.svg" alt="Tested with Pytest">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

Este projeto é um sistema de gestão de estoque e financeiro desenvolvido em Python, com foco total em robustez, qualidade de código e eficiência. A solução é desenhada para modernizar os processos de pequenas farmácias de bairro, substituindo controles manuais por uma ferramenta digital confiável e de simples utilização.

---

## ⚙️ Funcionalidades e Arquitetura

-   ✅ **Arquitetura Orientada a Objetos (POO):** O projeto é solidamente arquitetado usando Classes (`Product`, `Batch`, `User`) e princípios de Clean Code (SRP, DRY) para garantir um código organizado, manutenível e escalável.
-   ✅ **Fundação de Testes Robusta:** A qualidade é garantida por uma cultura de **Test-Driven Development (TDD)** com Pytest, cobrindo as camadas de utilitários, modelos de dados e lógica de negócio com testes unitários e de interação.
-   ✅ **Design de Software Avançado:** Implementação de padrões de design como **Injeção de Dependência** em módulos críticos para criar um código desacoplado, flexível e de fácil extensão.
-   ✅ **Modelo de Dados Relacional:** Schema de banco de dados (SQLite) projetado do zero para assegurar a integridade e o controle preciso de produtos, lotes e usuários.
-   ✅ **Automação de Entrada de Estoque:** Fluxo completo de importação de NF-e (XML), processando e persistindo os dados de novos produtos e lotes no banco de dados.
-   ✅ **Gestão de Usuários Segura:** Funcionalidade de cadastro e login de vendedores, com armazenamento seguro de PIN usando o algoritmo de hash **SHA-256**.

---

## 🧱 Tecnologias Utilizadas

-   **Linguagem Principal:** Python 3.12+
-   **Testes:** Pytest, unittest.mock
-   **Banco de Dados:** SQLite
-   **Bibliotecas Externas:** `pwinput`
-   **Bibliotecas Padrão:** `xml.etree.ElementTree`, `datetime`, `hashlib`, `logging`

---

## 🚀 Como Executar

1.  Clone o projeto e entre na pasta:
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
4.  Execute a aplicação:
    ```bash
    py main.py
    ```

---

## 🧪 Rodando os Testes

A qualidade do projeto é garantida por uma suíte de testes completa. Para executá-la, use o seguinte comando na raiz do projeto:

```bash
pytest -vv
```

---

## 🧩 Estrutura do Projeto

```
gestaoFarma_simples/
├── system/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── batch.py
│   │   ├── product.py
│   │   └── user.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── converters.py
│   │   ├── exceptions.py
│   │   ├── io_collectors.py
│   │   └── validators.py
│   ├── __init__.py
│   ├── database.py
│   └── security.py
├── tests/
│   ├── tests_models/
│   │   ├── __init__.py
│   │   ├── test_batch.py
│   │   └── test_product.py
│   │   └── test_user.py
│   ├── test_utils/
│   │   ├── __init__.py
│   │   ├── test_converters.py
│   │   ├── test_io_collectors.py
│   │   └── test_validators.py
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_database.py
│   └── test_security.py
├── .gitignore
├── main.py
├── README.md
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

## 📅 Histórico de Evolução do Projeto

### Fase 4: Garantia de Qualidade e Fundação de Testes [CONCLUÍDA]
* **22/09/2025 — Cobertura Total da Fundação:**
    - Conclusão da suíte de testes unitários para todas as camadas fundamentais do sistema (`utils`, `security`, `models`). 
    - Adoção de Test-Driven Development (TDD) com Pytest para garantir a robustez e o comportamento esperado de cada componente em isolamento. 
    - Implementação de testes de interação com `unittest.mock` e parametrização para validar a nova arquitetura do módulo de I/O.

### Fase 3: Operação de Vendas [EM ANDAMENTO]
* **09/08/2025 — Fase 3.3 (Conclusão da Lógica de Adição de Itens):**
    - Refatoração do modelo de dados para suportar o `id_lote_fisico` do fabricante, alinhando o sistema com os processos de negócio reais.
    - Implementação da lógica de validação de lote por 4 dígitos no ponto de venda.
    - Integração do sistema de auditoria para registrar desvios da regra PVPS.
    - Finalização da estratégia de "Produto Avulso" para vendas de itens não-cadastrados.
* **04/08/2025 — Fase 3.2 (Interface de Venda e Logging):**
    - Desenvolvimento da função `vendas.adicionar_item`, criando a primeira interface interativa para busca e seleção de produtos.
    - Implementação de um sistema de logging profissional e modular (`config_log.py`).
* **01/08/2025 — Fase 3.1 (Fundação de Vendas e Controle):**
    - Criação da classe `Item` com lógicas de negócio (`desconto`, `subtotal`).
    - Implementação do sistema de auditoria com a tabela `alertas_lote`.
    - Correção do fluxo de importação de NF-e.

### Fase 2: Gestão de Acessos e Refatoração para POO [CONCLUÍDA]
* **25/07/2025:** Finalização do fluxo completo de autenticação (cadastro e login) com hashing SHA-256.
* **24/07/2025:** Implementação da classe `Usuario` e design do schema para `pedidos` e `itens_pedido`.
* **20/07/2025:** Conclusão da refatoração para POO, com funções de banco de dados operando sobre objetos e extração da lógica para módulos.
* **16/07/2025:** Início da refatoração para Programação Orientada a Objetos com as classes `Produto` e `Lote`.
* **13/07/2025:** Implementação inicial do cadastro de usuários.

### Fase 1: Arquitetura de Dados [CONCLUÍDA]
* **11/07/2025:** Refatoração do banco de dados para um modelo relacional com as tabelas `produtos` e `lotes`.

### Fase 0: Fundação [CONCLUÍDA]
* **02/07/2025:** Criação do repositório e da estrutura inicial do projeto.

---

## 📌 Observações Finais

O **GestãoFarma Simples** foi desenvolvido com o usuário final em mente: pessoas não técnicas que precisam de uma ferramenta que funcione de forma direta e sem complicações. A filosofia do projeto é priorizar a simplicidade na interface e a robustez na lógica de automação, resolvendo uma dor real do pequeno comerciante com tecnologia acessível.

A arquitetura de dados e de software está sendo desenhada para espelhar as melhores práticas da indústria, garantindo não apenas a simplicidade, mas também a precisão, a segurança e a integridade das informações do negócio a longo prazo.