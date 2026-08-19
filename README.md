# Quantum-Resistant AI-Adaptive Cryptography System

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22011911.svg)](https://doi.org/10.5281/zenodo.22011911)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![NIST PQC](https://img.shields.io/badge/NIST-FIPS%20203%20%7C%20204-green.svg)](https://csrc.nist.gov/projects/post-quantum-cryptography)

> **An AI-adaptive Post-Quantum Cryptography (PQC) research prototype integrating NIST-standardized ML-KEM and ML-DSA with real-time system telemetry and anomaly detection.**

This project presents an end-to-end research prototype for **adaptive Post-Quantum Cryptography (PQC)**. It combines NIST-standardized **ML-KEM (FIPS 203)** and **ML-DSA (FIPS 204)** with machine learning models that dynamically select cryptographic parameters based on runtime system conditions.

The system can also detect anomalous behavior and automatically escalate the cryptographic security level when a potential threat is identified.

---

## 👥 Authors

### Rimsha Rani

**University of the Punjab, Lahore**
📧 [rimsha.rani@example.com](mailto:rimsharanii211@gmail.com)

### Uma Ammara

**University of the Punjab, Lahore**
📧 [uma.ammara@example.com](mailto:umeammara459@gmail.com)

---

## 🎯 Project Overview

Traditional cryptographic systems generally use fixed cryptographic parameters regardless of changing system conditions.

This research prototype explores an **AI-driven adaptive approach**, where cryptographic parameter selection responds dynamically to:

* CPU utilization
* Memory usage
* Network latency
* Runtime performance
* Detected anomalies
* Potential security threats

The system uses machine learning to balance **security, performance, and runtime efficiency**.

### Core Concept

```text
                         ┌─────────────────────────┐
                         │     Incoming Payload    │
                         └────────────┬────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────┐
                    │     AI Optimization Layer     │
                    │       Random Forest Model     │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │       PQC Cryptography         │
                    │     ML-KEM / ML-DSA Engine     │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │      Secure Data Channel       │
                    │       AES-256-GCM Layer        │
                    └───────────────────────────────┘
                                    ▲
                                    │
                    ┌───────────────┴───────────────┐
                    │       Threat Detection        │
                    │      Isolation Forest Model   │
                    └───────────────────────────────┘
```

---

## ✨ Key Features

### 🤖 AI-Based Cryptographic Optimization

A **Random Forest classifier** evaluates runtime telemetry such as:

* CPU load
* Memory utilization
* Network latency
* System performance metrics

Based on these inputs, the model selects an appropriate PQC parameter set.

### 🛡️ Automated Threat Escalation

An **Isolation Forest anomaly detector** continuously monitors runtime behavior.

When suspicious activity is detected, the system automatically escalates cryptographic protection to the highest supported security level:

**ML-KEM-1024 — NIST Security Level 5**

### 🔐 Post-Quantum Cryptography

The prototype integrates:

* **ML-KEM — FIPS 203**
* **ML-DSA — FIPS 204**
* AES-256-GCM for symmetric encryption

### 🌐 End-to-End Communication

A socket-based client/server demonstration illustrates secure communication using hybrid post-quantum and symmetric cryptography.

### 📊 Benchmarking

The project includes an empirical benchmark dataset containing **601 rows** of performance measurements used for model development and evaluation.

---

# 🏗️ Architecture

The system consists of five primary components:

| Component             | Description                                              |
| --------------------- | -------------------------------------------------------- |
| **Crypto Engine**     | Implements ML-KEM, ML-DSA, and security escalation logic |
| **Telemetry Module**  | Collects runtime system performance metrics              |
| **AI Optimization**   | Uses Random Forest for adaptive parameter selection      |
| **Threat Detection**  | Uses Isolation Forest for anomaly detection              |
| **Application Layer** | Provides socket-based sender/receiver demonstration      |

---

# 📂 Repository Structure

```text
quantum-resistant-ai-crypto/
│
├── src/
│   ├── crypto/
│   │   └── # ML-KEM & ML-DSA routines and escalation logic
│   │
│   ├── telemetry/
│   │   └── # Real-time system performance monitoring
│   │
│   ├── benchmarking/
│   │   └── # Dataset generation and benchmarking scripts
│   │
│   ├── ai_models/
│   │   └── # Random Forest & Isolation Forest training pipeline
│   │
│   └── app/
│       └── # Socket-based client/server demonstration
│
├── data/
│   └── # 601-row empirical benchmark dataset
│
├── models/
│   └── # Serialized ML models (.pkl)
│
├── results/
│   └── # Visualizations and performance charts
│
├── liboqs-python/
│   └── # Open Quantum Safe Python bindings
│
├── requirements.txt
└── README.md
```

---

# 📊 Performance Benchmarks

## Machine Learning Performance

| Metric                               |        Result |
| ------------------------------------ | ------------: |
| Random Forest Model Accuracy         |    **96.69%** |
| Threat Detection Overhead            | **< 14.2 ms** |
| Isolation Forest False Positive Rate |    **< 1.2%** |

## PQC Benchmark Results

| Primitive       | Function          | Public Key | Ciphertext / Signature | Mean Execution Time | NIST Level |
| --------------- | ----------------- | ---------: | ---------------------: | ------------------: | ---------: |
| **ML-KEM-512**  | Encapsulation     |      800 B |                  768 B |             0.42 ms |    Level 1 |
| **ML-KEM-768**  | Encapsulation     |    1,184 B |                1,088 B |             0.68 ms |    Level 3 |
| **ML-KEM-1024** | Encapsulation     |    1,568 B |                1,568 B |             1.05 ms |    Level 5 |
| **ML-DSA-44**   | Digital Signature |    1,312 B |                2,420 B |             1.28 ms |    Level 2 |
| **ML-DSA-65**   | Digital Signature |    1,952 B |                3,309 B |             2.15 ms |    Level 3 |
| **ML-DSA-87**   | Digital Signature |    2,592 B |                4,627 B |             3.42 ms |    Level 5 |

> **Note:** Benchmark values are based on the project's empirical evaluation environment and dataset.

---

# 🧠 Machine Learning Pipeline

The adaptive cryptography layer consists of two machine learning components.

### Random Forest — Optimization Classifier

The Random Forest model maps runtime telemetry to the most suitable cryptographic parameter set.

```text
Runtime Telemetry
       │
       ├── CPU Load
       ├── Memory Usage
       └── Latency
              │
              ▼
       Random Forest
              │
              ▼
   Optimal PQC Parameter Set
```

### Isolation Forest — Threat Detection

The Isolation Forest model monitors runtime behavior and identifies anomalous activity.

```text
Runtime Behavior
       │
       ▼
Isolation Forest
       │
       ├── Normal ──────► Continue Current Security Level
       │
       └── Anomaly ─────► Escalate Security
                              │
                              ▼
                         ML-KEM-1024
```

---

# 🔒 Security Escalation

Under normal operating conditions, the AI optimization layer selects a cryptographic configuration based on system performance.

When the threat detector identifies anomalous behavior, the system overrides the optimization decision and increases the security level.

```text
Normal Operation
       │
       ▼
AI-Based Parameter Selection
       │
       ▼
Appropriate PQC Security Level


Threat Detected
       │
       ▼
Isolation Forest Alert
       │
       ▼
Security Escalation
       │
       ▼
ML-KEM-1024
```

This design prioritizes security when suspicious runtime behavior is detected.

---

# ⚡ Quick Start

## 1. Clone the Repository

```bash
git clone --recurse-submodules https://github.com/UmaAmmara/quantum-resistant-ai-crypto.git

cd quantum-resistant-ai-crypto
```

If the repository was cloned without submodules:

```bash
git submodule update --init --recursive
```

---

## 2. Install Open Quantum Safe Python Bindings

```bash
cd liboqs-python

pip install .

cd ..
```

---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Running the Prototype

The project includes a socket-based sender/receiver demonstration.

Open **two terminal windows**.

### Terminal 1 — Receiver

```bash
python src/app/receiver.py
```

### Terminal 2 — Sender

```bash
python src/app/sender.py
```

The sender and receiver demonstrate the end-to-end secure communication workflow using the project's hybrid cryptographic architecture.

---

# 🧪 Research Components

The repository includes components for:

* Post-quantum key encapsulation
* Post-quantum digital signatures
* Runtime telemetry collection
* Cryptographic benchmarking
* AI-based parameter optimization
* Anomaly detection
* Security escalation
* AES-256-GCM encryption
* Socket-based secure communication
* Dataset generation
* Model training and evaluation

---

# 📚 Standards & Technologies

### Cryptography

* **NIST FIPS 203 — ML-KEM**
* **NIST FIPS 204 — ML-DSA**
* **AES-256-GCM**

### Machine Learning

* Random Forest
* Isolation Forest
* Python / scikit-learn

### Implementation

* Python 3.10+
* Open Quantum Safe
* liboqs-python
* Socket programming

---

# 📈 Research Results

The prototype demonstrates the feasibility of combining machine learning with post-quantum cryptography for adaptive security.

Key reported results include:

* **96.69%** Random Forest classification accuracy
* **< 14.2 ms** threat escalation latency
* **< 1.2%** Isolation Forest false-positive rate
* Support for **NIST security Levels 1, 3, and 5**
* End-to-end hybrid PQC + AES-256-GCM communication

---

# 📦 Dataset

The repository contains an empirical benchmark dataset with **601 rows** of cryptographic and system-performance measurements.

The dataset is used to support:

1. AI model training
2. Cryptographic parameter classification
3. Performance analysis
4. Benchmark comparison
5. Evaluation of adaptive security decisions

---

# 🔬 Research Scope

This repository is intended as a **research prototype** exploring the intersection of:

* Post-Quantum Cryptography
* Artificial Intelligence
* Adaptive Security
* Anomaly Detection
* Cryptographic Performance Optimization
* Secure Network Communication

The implementation is designed for experimentation, benchmarking, and academic research rather than direct deployment in production security infrastructure.

---

# 📖 Citation

If you use this project, dataset, or research results in academic work, please cite the Zenodo publication:

```bibtex
@software{rani_ammara_2026_zenodo,
  author       = {Rimsha Rani and Uma Ammara},
  title        = {Quantum-Resistant AI-Adaptive Cryptography System: Benchmark Dataset and Prototype},
  month        = aug,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.22011911},
  url          = {https://doi.org/10.5281/zenodo.22011911}
}
```

**DOI:** https://doi.org/10.5281/zenodo.22011911

---

# 📄 License

This project is distributed under the **MIT License**.

See the `LICENSE` file for more information.

---

# ⚠️ Disclaimer

This project is an **academic and research prototype**.

The reported performance metrics, machine learning accuracy, detection rates, and cryptographic benchmarks are dependent on the experimental environment and dataset used during development.

The system should undergo additional security auditing, testing, and cryptographic review before being considered for production deployment.

---

## ⭐ Acknowledgment

This project explores how **AI-driven adaptation can complement post-quantum cryptographic mechanisms** to create security systems that dynamically respond to changing runtime conditions and potential threats.
