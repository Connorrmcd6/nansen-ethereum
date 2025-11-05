# Ethereum On-Chain Analytics Pipeline — Ingestion Component

## Overview

This repository demonstrates the **ingestion component** of a pipeline designed to produce valuable labels for blockchain addresses. These labels help investors better understand on-chain activity and make smarter decisions.

- **Architecture design**: See [`Architecture.md`](./Architecture.md) for a detailed overview, technology choices, and future roadmap.
- **Working code sample**: This repo implements the ingestion pipeline, exporting Ethereum blockchain data and loading it into BigQuery.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Connorrmcd6/nansen-ethereum.git
cd nansen
```

### 2. Create and Activate a Python 3.11 Virtual Environment

Make sure Python 3.11 is installed on your system.  
You can check with:

```bash
python3.11 --version
```

Create the virtual environment using Python 3.11:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

> **Note:**  
> This project requires Python 3.11 because `ethereum-etl` is not compatible with Python 3.13.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare Google Cloud Credentials

- Download your GCP service account key as `gcp-key.json` and place it in the project root.

### 5. Run the Ingestion Script

```bash
python scripts/ingest_eth_blocks.py
```

This will:

- Export Ethereum blocks and transactions for a small block range.
- Load the transactions into your specified BigQuery table using a strict schema.

---

## Architecture Overview

The full pipeline design, including ingestion, transformation, and analytics layers, is described in [`Architecture.md`](./Architecture.md).

**Author:** Connor McDonald  
**Date:** November 2025
