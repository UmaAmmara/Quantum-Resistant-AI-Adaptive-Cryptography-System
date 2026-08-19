# Quantum-Resistant AI-Adaptive Cryptography System

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22011911.svg)](https://doi.org/10.5281/zenodo.22011911)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![NIST PQC](https://img.shields.io/badge/NIST-FIPS%20203%20%7C%20204-green.svg)](https://csrc.nist.gov/projects/post-quantum-cryptography)

An end-to-end research prototype implementing an adaptive Post-Quantum Cryptography (PQC) framework. Integrating **NIST FIPS 203 (ML-KEM)** and **FIPS 204 (ML-DSA)** with machine learning, this system dynamically selects optimal cryptographic parameters based on runtime telemetry and automatically escalates security strength upon detecting anomalies.

---

## 👥 Authors

* **Rimsha Rani**  
  University of Central Punjab, Lahore  
  📧 Email: [rimsha.rani@example.com](mailto:rimsha.rani@example.com)

* **Uma Ammara**  
  University of the Punjab, Lahore  
  📧 Email: [uma.ammara@example.com](mailto:uma.ammara@example.com)

---

## 📌 Features & Architecture

* **Dynamic Optimization:** A Random Forest model evaluates CPU load, memory, and latency to select the best PQC parameter set.
* **Threat Escalation:** An Isolation Forest anomaly detector forces maximum bit-strength encryption (**ML-KEM-1024**) when attacks are identified.
* **End-to-End Prototype:** Includes socket-based transmission using hybrid PQC and AES-256-GCM symmetric encryption.

```text
Incoming Payload ➔ AI Optimization Layer (Random Forest) ➔ PQC Engine (ML-KEM / ML-DSA)
                                  ▲
                       Threat Detector (Isolation Forest)
📂 Repository StructurePlaintextquantum-resistant-ai-crypto/
├── src/
│   ├── crypto/          # ML-KEM & ML-DSA routines and escalation logic
│   ├── telemetry/       # Real-time system performance monitoring
│   ├── benchmarking/    # Dataset generation & benchmarking scripts
│   ├── ai_models/       # ML training pipeline (Random Forest & Isolation Forest)
│   └── app/             # Socket client/server demonstration scripts
├── data/                # 601-row empirical benchmark dataset
├── models/              # Serialized ML models (.pkl)
├── results/             # Visualizations and performance charts
├── liboqs-python/       # Open Quantum Safe Python bindings
└── requirements.txt     # Python dependencies
📊 Performance BenchmarksModel Accuracy: 96.69% (Random Forest optimization classifier)Detection Overhead: < 14.2 ms escalation latencyFalse Positive Rate: < 1.2% (Isolation Forest)Primitive VariantFunctionPublic KeyCiphertext / SigMean Exec TimeNIST LevelML-KEM-512Encapsulation800 B768 B0.42 msLevel 1ML-KEM-768Encapsulation1,184 B1,088 B0.68 msLevel 3ML-KEM-1024Encapsulation1,568 B1,568 B1.05 msLevel 5ML-DSA-44Digital Signature1,312 B2,420 B1.28 msLevel 2ML-DSA-65Digital Signature1,952 B3,309 B2.15 msLevel 3ML-DSA-87Digital Signature2,592 B4,627 B3.42 msLevel 5⚡ Quick Start Guide1. InstallationBashgit clone --recurse-submodules [https://github.com/UmaAmmara/quantum-resistant-ai-crypto.git](https://github.com/UmaAmmara/quantum-resistant-ai-crypto.git)
cd quantum-resistant-ai-crypto

cd liboqs-python && pip install . && cd ..
pip install -r requirements.txt
2. Run Prototype DemoOpen two terminal windows to execute the socket-based prototype:Terminal 1 (Receiver): python src/app/receiver.pyTerminal 2 (Sender): python src/app/sender.py📜 CitationCode snippet@software{rani_ammara_2026_zenodo,
  author       = {Rimsha Rani and Uma Ammara},
  title        = {Quantum-Resistant AI-Adaptive Cryptography System: Benchmark Dataset and Prototype},
  month        = aug,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.22011911},
  url          = {[https://doi.org/10.5281/zenodo.22011911](https://doi.org/10.5281/zenodo.22011911)}
}
📄 LicenseDistributed under the MIT License.
