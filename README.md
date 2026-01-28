# GestaoFarma Simples: High-Performance ERP & Data Pipeline Architecture

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

## Technical Overview
GestaoFarma Simples is an enterprise-grade ERP designed for the pharmaceutical sector, engineered with a focus on data integrity, high-performance persistence, and decoupled architecture. This project represents a seven-month deep dive into Clean Architecture and Data Engineering, implementing complex ETL pipelines, regulatory data normalization, and optimized storage engines.

---

## Core Engineering Pillars

### 1. Advanced ETL & Data Ingestion Pipelines
The core of the system’s intelligence resides in its ability to ingest and transform heterogeneous data sources into a unified relational schema.

* **NFE Tax Document Orchestration (XML Parser):** - Implemented a specialized parser for Brazilian Fiscal Documents (NF-e) using high-efficiency XML tree traversal.
    - **Logic:** Automated extraction of product metadata, tax codes (CFOP/CST), and batch information.
    - **Inventory Linkage:** Integrated a transformation layer that maps tax document entries directly to FIFO-based inventory batches, ensuring real-time cost averaging and stock accuracy.
* **CMED Regulatory Data Normalization:** - Engineered an ingestion engine for CMED (Regulatory Chamber of the Pharmaceutical Market) datasets.
    - **Challenges Resolved:** Handling large-scale external data with inconsistent formatting, implementing data sanitization, and executing bulk upsert operations to synchronize local pricing with national regulatory standards.
    - **Async Processing:** Utilizes a background threading model managed by a `DispatcherService` to ensure zero UI-blocking during heavy ingestion cycles.

### 2. Persistence Engineering & B-Tree Optimization
The database layer was designed to prioritize analytical throughput and data consistency.
* **Indexing Strategy:** Strategic implementation of B-Tree indexes (e.g., `idx_orders_order_date`) to shift search complexity from $O(n)$ to $O(\log n)$, crucial for analytical reporting over expanding datasets.
* **Write-Ahead Logging (WAL):** Configuration of the SQLite engine in WAL mode to facilitate high-concurrency environments, allowing simultaneous read/write operations without transactional locks.
* **Financial Precision:** System-wide enforcement of the `Decimal` type, eliminating binary floating-point rounding errors in revenue and mid-ticket calculations.

### 3. Clean Architecture & Decoupling
* **Dependency Inversion (DIP):** Strict adherence to unidirectional dependency flow. High-level business rules (Services) are completely agnostic of low-level implementation details (Repositories/UI).
* **Event-Driven Architecture:** Implementation of the Observer Pattern via a centralized Dispatcher to manage cross-module communication and asynchronous state updates.

---

## Technical Stack
* **Core:** Python 3.12+ (Utilizing `__slots__` for memory footprint reduction and strict type hinting).
* **Database:** SQLite (Engineered with custom adapters for date/decimal persistence).
* **Testing:** Robust TDD environment using **Pytest** for unit and integration verification.
* **Tooling:** Batch-based environment management for multi-station portability and low-level page analysis.

---

## Documentation (Portuguese)
For a detailed version in Brazilian Portuguese, please refer to [README-ptbr.md](./README-ptbr.md).