# 薬 GestãoFarma Simples — Sistema de Gestão para Farmácias

Este projeto tem como objetivo desenvolver um sistema de gestão de estoque e financeiro em Python, com foco total em simplicidade e eficiência. A solução é desenhada para atender às necessidades de pequenas farmácias de bairro, onde os processos ainda são, em grande parte, manuais e ineficientes, visando um público-alvo não técnico.

---

## ⚙️ Funcionalidades Atuais

* ✅ **Leitura e Análise de NF-e:** O sistema consegue ler e interpretar os dados de produtos de um arquivo XML de Nota Fiscal Eletrônica.
* ✅ **Gravação Inteligente no Banco de Dados:** A lógica de "UPSERT" (inserir ou atualizar) foi implementada, permitindo que o sistema adicione produtos novos e atualize a quantidade e o custo de produtos existentes.
* ✅ **Assistente de Cadastro Interativo:** O sistema identifica produtos novos e interage com o usuário para solicitar dados essenciais que não constam no XML, como preço de venda e data de validade.
* ✅ **Controle de Versão:** O projeto está totalmente configurado para versionamento com Git e GitHub.
* ➡️ **Próxima Fase (Gestão de Vendas):** A próxima grande etapa é a implementação do registro de vendas, com baixa de estoque.
* 📝 **Em Planejamento:** Alertas de estoque baixo, controle de validade e desenvolvimento de uma Interface Gráfica (GUI).

---

## 🧱 Tecnologias Utilizadas

-   **Python 3.12+**
-   **VS Code**

### Bibliotecas Padrão:

-   `sqlite3` (Banco de Dados)
-   `xml.etree.ElementTree` (Leitura de XML)
-   `os`, `pathlib`, `time`

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

-   **02/07/2025** — Fase 0 (Fundação): Criação do repositório, estrutura inicial do projeto, documentação e implementação do leitor de NF-e (XML).
-   **06/07/2025** — Fase 1 (Entrada de Estoque): Conclusão da automação de entrada com a implementação do "Assistente de Cadastro" interativo e a lógica de "UPSERT" no banco de dados.

---

## 📌 Observações Finais

O **GestãoFarma Simples** foi desenvolvido com o usuário final em mente: pessoas não técnicas que precisam de uma ferramenta que funcione de forma direta e sem complicações. A filosofia do projeto é priorizar a simplicidade na interface e a robustez na lógica de automação, resolvendo uma dor real do pequeno comerciante com tecnologia acessível.

O projeto serve como um case prático de desenvolvimento de um MVP (Minimum Viable Product), partindo de um problema familiar para uma potencial solução de negócio escalável.