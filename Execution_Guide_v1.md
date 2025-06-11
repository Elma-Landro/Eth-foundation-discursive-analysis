
# ETH Foundation Discursive Analysis — Local Execution Guide

This short guide explains how to locally execute the full pipeline for corpus analysis and verification.

---

## 1️⃣ Prerequisites

- You have already cloned the repository locally using:

```bash
git clone https://github.com/Elma-Landro/Eth-foundation-discursive-analysis.git
```

- You have Python 3 installed on your system.

You can check by running:

```bash
python3 --version
```

If not installed, use your package manager (for example on Ubuntu: `sudo apt install python3`).

---

## 2️⃣ Enter your repository folder

```bash
cd Eth-foundation-discursive-analysis
```

---

## 3️⃣ Running the Corpus Integrity Checker

You can verify that your corpus contains all expected `.txt` files.

```bash
python3 scripts/corpus_file_counter.py
```

Expected output:

```
Total .txt files found in './data/corpus_raw/individual_articles/': 567
```

This ensures that your full Ethereum Foundation corpus is properly loaded.

---

## 4️⃣ Running the full analysis pipeline

You can execute the full lexical pipeline using the Jupyter Notebook provided:

### A. Install Jupyter (if not already installed):

```bash
pip install notebook
```

or via Anaconda if you prefer.

### B. Launch Jupyter Notebook:

```bash
jupyter notebook
```

### C. Open and run the notebook:

Open `notebooks/ETH_Foundation_Master_Pipeline.ipynb` in your browser and execute all cells step by step.

---

## 5️⃣ Outputs location

- All outputs (CSV files, word clouds, co-occurrence networks, visualizations) are saved automatically in:

```
outputs/
```

---

✅ You are now fully operational for local reproducible analysis.

---

*For any extensions or future modules, follow the same local execution logic after pulling updates from GitHub.*
