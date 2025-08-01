# 薬 GestãoFarma Simples — Sistema de Gestão para Farmácias

Este projeto tem como objetivo desenvolver um sistema de gestão de estoque e financeiro em Python, com foco total em simplicidade e eficiência. A solução é desenhada para atender às necessidades de pequenas farmácias de bairro, onde os processos ainda são, em grande parte, manuais e ineficientes, visando um público-alvo não técnico.

---

## ⚙️ Funcionalidades Atuais

-   ✅ **Arquitetura Orientada a Objetos (POO):** O projeto é solidamente arquitetado usando Classes (`Produto`, `Lote`, `Usuario`, `Item`), tornando o código organizado, reutilizável e alinhado com as melhores práticas de engenharia.
-   ✅ **Modelo de Dados Relacional e Robusto:** Implementado um schema em SQLite com tabelas para `produtos`, `lotes`, `usuarios`, e a fundação para `pedidos`, `itens_pedido` e `alertas_lote`, garantindo a integridade e o controle dos dados.
-   ✅ **Lógica de Negócio Inteligente:** A classe `Item` encapsula regras de negócio complexas, incluindo:
    -   Cálculo de subtotal.
    -   Um sistema de **descontos dinâmicos** que se ajusta com base na proximidade da data de validade, com uma **"rede de segurança"** para nunca vender um produto abaixo do seu preço de custo.
-   ✅ **Sistema de Auditoria (PVPS):** O sistema possui uma fundação completa para auditar desvios na regra de negócio "Primeiro que Vence, Primeiro que Sai", registrando ocorrências para análise gerencial.
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
│   └── teste1_NFE.xml (e outros arquivos de exemplo)
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

## 📅 Histórico de Atualizações

-   **02/07/2025 — Fase 0 (Fundação):** Criação do repositório e da estrutura inicial do projeto.
-   **11/07/2025 — Fase 1 (Arquitetura de Dados):** Refatoração do banco de dados para um modelo relacional (`produtos` + `lotes`).
-   **13/07/2025 — Fase 2 (Início - Gestão de Usuários):** Criação da tabela `usuarios` e implementação do cadastro de vendedor com hashing de PIN.
-   **16/07/2025 — Fase 2 (Refatoração para POO):** Decisão arquitetônica e refatoração do sistema para Programação Orientada a Objetos, com a criação das classes `Produto` e `Lote` e a modularização da lógica de importação e validação.
-   **20/07/2025 — Fase 2 (Refatoração para POO - Parte 2):** Conclusão da refatoração para POO nos módulos de banco de dados e importação" -m "- Funções em `database.py` (buscar_produto, produtos_existentes) foram atualizadas para operar com objetos Produto. A lógica de importação foi extraída do `main.py` para o novo módulo `importador_nfe.py` e refatorada para usar a nova arquitetura de objetos."
-   **24/07/2025 — Fase 2 (Gestão de Usuários e Vendas):** Implementação da `class Usuario` e da função de `login` completa. Finalização do schema do banco de dados com o design das tabelas `pedidos` e `itens_pedido`.
-   **25/07/2025 — Fase 2 (Conclusão - Gestão de Acessos):** Finalização da arquitetura POO e implementação do fluxo completo de autenticação, incluindo cadastro (`cadastro_usuario`) e `login()` com hashing de PIN (SHA-256).
-   ➡️ **Início da Fase 3 (Operação de Vendas):** O próximo passo é o desenho e a implementação do schema de banco de dados para transações (`pedidos` e `itens_pedido`).
-   **01/08/2025 — Fase 3 (Fundação de Vendas e Controle):** Início da implementação do Ponto de Venda.
    -   Criação da classe `Item` para encapsular a lógica de um item de venda, com os métodos `calcular_subtotal()` e `desconto()`.
    -   Implementação do sistema de auditoria para desvios da regra PVPS, com a criação da tabela `alertas_lote` e da função `registrar_alerta_lote()`.
    -   Correção e finalização do fluxo de importação de NF-e, garantindo o salvamento dos produtos no banco de dados.
-   ➡️ **Próximo Passo (Fase 3.3):** Desenvolvimento da função `carrinho()` no módulo `vendas.py` para orquestrar a busca e adição de itens à venda.

---

## 📌 Observações Finais

O **GestãoFarma Simples** foi desenvolvido com o usuário final em mente: pessoas não técnicas que precisam de uma ferramenta que funcione de forma direta e sem complicações. A filosofia do projeto é priorizar a simplicidade na interface e a robustez na lógica de automação, resolvendo uma dor real do pequeno comerciante com tecnologia acessível.

A arquitetura de dados e de software está sendo desenhada para espelhar as melhores práticas da indústria, garantindo não apenas a simplicidade, mas também a precisão, a segurança e a integridade das informações do negócio a longo prazo.