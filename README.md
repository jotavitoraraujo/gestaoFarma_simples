# 薬 GestãoFarma Simples — Sistema de Gestão para Farmácias

Este projeto tem como objetivo desenvolver um sistema de gestão de estoque e financeiro em Python, com foco total em simplicidade e eficiência. A solução é desenhada para atender às necessidades de pequenas farmácias de bairro, onde os processos ainda são, em grande parte, manuais e ineficientes, visando um público-alvo não técnico.

---

## ⚙️ Funcionalidades Atuais

-   ✅ **Arquitetura Orientada a Objetos (POO):** O projeto é solidamente arquitetado usando Classes (`Produto`, `Lote`, `Usuario`, `Item`), tornando o código organizado, reutilizável e alinhado com as melhores práticas de engenharia.
-   ✅ **Modelo de Dados Relacional e Robusto:** Implementado um schema em SQLite com tabelas para `produtos`, `lotes`, `usuarios`, e a fundação para `pedidos`, `itens_pedido` e `alertas_lote`, garantindo a integridade e o controle dos dados.
-   ✅ **Interface de Venda Interativa:** O sistema possui um fluxo de terminal para adicionar itens a uma venda, com busca de produtos por nome, apresentação de menu dinâmico ordenado por validade (PVPS) e validação robusta de inputs do usuário.
-   ✅ **Lógica de Negócio Inteligente:** A classe `Item` encapsula regras de negócio complexas, incluindo cálculo de subtotal e um sistema de descontos dinâmicos com "rede de segurança" contra prejuízos.
-   ✅ **Sistema de Auditoria e Observabilidade:** O sistema possui uma fundação completa para auditar desvios da regra PVPS. Além disso, utiliza um sistema de logging profissional que separa os logs de usuário (exibidos no console) dos logs técnicos detalhados (salvos em arquivo).
-   ✅ **Automação de Entrada de Estoque:** O sistema realiza o fluxo completo de importação de NF-e, processando os dados e persistindo os novos produtos e lotes no banco de dados.
-   ✅ **Gestão de Usuários Segura:** Funcionalidade completa de cadastro e login de vendedores, com validação de entradas e armazenamento seguro do PIN usando o algoritmo de hash **SHA-256**.

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
-   `logging` (Sistema de Logs)
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
│   ├── farmacia.db
│   └── gestao_farma.log
│
├── sistema/
│   ├── __init__.py
│   ├── database.py
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── item.py
│   │   ├── lote.py
│   │   ├── produto.py
│   │   └── usuario.py
│   └── modulos/
│       ├── __init__.py
│       ├── config_log.py
│       ├── importador_nfe.py
│       ├── relatorios.py
│       ├── users.py
│       ├── validadores_input.py
│       └── vendas.py
│
├── venv/
├── .gitignore
├── LICENSE
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