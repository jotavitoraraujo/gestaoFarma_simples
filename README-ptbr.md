# GestaoFarma Simples: ERP e Arquitetura de Pipelines de Dados

<p align="center">
  <img src="./assets/gestaofarma_simples_logo_v2.png" alt="Logo do GestaoFarma Simples" width="200"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Tested%20with-Pytest-green.svg" alt="Tested with Pytest">
  <img src="https://img.shields.io/badge/Design%20Patterns-Repository%2C%20DI%2C%20VO-blueviolet" alt="Design Patterns">
  <img src="https://img.shields.io/badge/Architecture-Clean%20Layers-orange" alt="Architecture">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

## Visão Geral
O **GestaoFarma Simples** é um sistema de ERP de nível corporativo projetado para o setor farmacêutico, com foco em integridade de dados, persistência de alta performance e arquitetura desacoplada. Este projeto consolida 7 meses de engenharia, implementando pipelines de ETL complexos, normalização de dados regulatórios e motores de armazenamento otimizados.

---

## Pilares de Engenharia

### 1. Pipelines de ETL e Ingestão de Dados
A inteligência central do sistema reside na sua capacidade de ingerir e transformar fontes de dados heterogêneas em um esquema relacional unificado.

* **Orquestração de Documentos Fiscais (NFE XML Parser):** - Desenvolvimento de um parser especializado para Notas Fiscais Eletrônicas (NF-e) utilizando travessia eficiente de árvores XML.
    - **Lógica:** Extração automatizada de metadados de produtos, códigos fiscais (CFOP/CST) e informações de lote.
    - **Vínculo de Inventário:** Camada de transformação que mapeia entradas de documentos fiscais diretamente para lotes de estoque baseados em FIFO, garantindo precisão no custo médio e saldo.
* **Normalização de Dados Regulatórios (CMED):** - Motor de ingestão para bases de dados da CMED (Câmara de Regulação do Mercado de Medicamentos).
    - **Desafios Resolvidos:** Tratamento de dados externos em larga escala com formatação inconsistente, implementação de sanitização de dados e execução de operações de *bulk upsert* para sincronização de preços.
    - **Processamento Assíncrono:** Uso de threading gerenciado por um `DispatcherService` para garantir latência zero na interface durante ciclos pesados de ingestão.

### 2. Engenharia de Persistência e Otimização de B-Trees
A camada de banco de dados foi projetada para priorizar a vazão analítica e a consistência.
* **Estratégia de Indexação:** Implementação de índices B-Tree (ex: `idx_orders_order_date`) para converter a complexidade de busca de $O(n)$ para $O(\log n)$.
* **Write-Ahead Logging (WAL):** Configuração do SQLite em modo WAL para suportar ambientes de alta concorrência, permitindo operações simultâneas de leitura e escrita.
* **Precisão Financeira:** Uso sistemático de `Decimal` em todo o sistema, eliminando erros de arredondamento de ponto flutuante em cálculos de faturamento e ticket médio.

### 3. Arquitetura Limpa e Desacoplamento
* **Inversão de Dependência (DIP):** Fluxo de dependência unidirecional onde regras de negócio de alto nível (Services) são agnósticas aos detalhes de infraestrutura (Repositories/UI).
* **Arquitetura Baseada em Eventos:** Implementação do padrão Observer para gerenciar a comunicação entre módulos e atualizações de estado assíncronas.

---

## Stack Tecnológica
* **Linguagem:** Python 3.12+ (uso de `__slots__` para redução de footprint de memória).
* **Banco de Dados:** SQLite (com adaptadores customizados para persistência de tipos complexos).
* **Qualidade:** Ambiente TDD robusto com **Pytest** para verificações unitárias e de integração.