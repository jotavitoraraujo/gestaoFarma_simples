# 薬 GestãoFarma Simples — Sistema de Gestão para Farmácias

Este projeto tem como objetivo desenvolver um sistema de gestão de estoque e financeiro em Python, com foco total em simplicidade e eficiência. A solução é desenhada para atender às necessidades de pequenas farmácias de bairro, onde os processos ainda são, em grande parte, manuais e ineficientes, visando um público-alvo não técnico.

---

## ⚙️ Funcionalidades Atuais

-   ✅ **Modelo de Dados Relacional:** Implementado um schema robusto com duas tabelas (`produtos` e `lotes`) para garantir a integridade dos dados e permitir um controle de estoque por lote, incluindo custo e validade específicos para cada compra.
-   ✅ **Leitura e Análise de NF-e:** O sistema consegue ler e interpretar os dados de produtos de um arquivo XML de Nota Fiscal Eletrônica.
-   ✅ **Assistente de Cadastro Interativo:** O sistema identifica produtos novos e interage com o usuário para obter dados essenciais, como preço de venda e data de validade.
-   ✅ **Validação de Entrada Robusta:** A entrada de dados do usuário para preço e data é validada para garantir que os valores sejam lógicos (preços positivos, datas futuras) e para aceitar formatos comuns (preços com vírgula, datas no padrão D/M/A).
-   ✅ **Controle de Versão:** O projeto está totalmente configurado para versionamento com Git e GitHub.
-   ➡️ **Próxima Fase (Gestão de Vendas):** A próxima grande etapa é a implementação do registro de vendas, com baixa de estoque baseada na lógica PVPS (Primeiro que Vence, Primeiro que Sai).

---

## 🧱 Tecnologias Utilizadas

-   **Python 3.12+**
-   **VS Code**

### Bibliotecas Padrão:

-   `sqlite3` (Banco de Dados)
-   `xml.etree.ElementTree` (Leitura de XML)
-   `datetime` (Manipulação de Datas)
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
│       └── leitor_xml.py
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

-   **02/07/2025 — Fase 0 (Fundação):** Criação do repositório, estrutura inicial do projeto, documentação e implementação do leitor de NF-e (XML).
-   **11/07/2025 — Fase 1 (Arquitetura e Entrada de Dados):** Refatoração do banco de dados para um modelo relacional (`produtos` + `lotes`). Implementação do fluxo completo de importação de NF-e, incluindo o "Assistente de Cadastro" com validação de dados para novos produtos.

---

## 📌 Observações Finais

O **GestãoFarma Simples** foi desenvolvido com o usuário final em mente: pessoas não técnicas que precisam de uma ferramenta que funcione de forma direta e sem complicações. A filosofia do projeto é priorizar a simplicidade na interface e a robustez na lógica de automação, resolvendo uma dor real do pequeno comerciante com tecnologia acessível.

A arquitetura de dados foi desenhada para espelhar a realidade da gestão de lotes, garantindo não apenas a simplicidade, mas também a precisão e a integridade das informações do negócio a longo prazo.