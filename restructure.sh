#!/bin/bash
# Run this from the root of your repo (quantum-resistant-ai-crypto/)
# This reorganizes the flat file structure into a professional layout.

set -e  # stop on first error

echo "Creating folder structure..."
mkdir -p src/crypto src/telemetry src/benchmarking src/ai_models src/app
mkdir -p data models results docs

echo "Moving crypto files..."
[ -f kyber_test.py ] && git mv kyber_test.py src/crypto/kyber_test.py
[ -f dilithium_test.py ] && git mv dilithium_test.py src/crypto/dilithium_test.py
[ -f key_escalation.py ] && git mv key_escalation.py src/crypto/key_escalation.py

echo "Moving telemetry files..."
[ -f telemetry_collector.py ] && git mv telemetry_collector.py src/telemetry/telemetry_collector.py

echo "Moving benchmarking files..."
[ -f benchmark_kyber.py ] && git mv benchmark_kyber.py src/benchmarking/benchmark_kyber.py
[ -f benchmark_dilithium.py ] && git mv benchmark_dilithium.py src/benchmarking/benchmark_dilithium.py
[ -f eda.py ] && git mv eda.py src/benchmarking/eda.py
[ -f merge_clean_dataset.py ] && git mv merge_clean_dataset.py src/benchmarking/merge_clean_dataset.py
[ -f setup_project.py ] && git mv setup_project.py src/benchmarking/setup_project.py

echo "Moving AI model files..."
[ -f train_model.py ] && git mv train_model.py src/ai_models/train_model.py
[ -f attack_detector.py ] && git mv attack_detector.py src/ai_models/attack_detector.py

echo "Moving app files..."
[ -f chat_app_sender.py ] && git mv chat_app_sender.py src/app/sender.py
[ -f chat_app_receiver.py ] && git mv chat_app_receiver.py src/app/receiver.py
[ -f receiver.py ] && git mv receiver.py src/app/receiver.py

echo "Moving model files (.pkl) into models/..."
[ -f ai_model.pkl ] && git mv ai_model.pkl models/ai_model.pkl
[ -f attack_detector.pkl ] && git mv attack_detector.pkl models/attack_detector.pkl

echo "Cleaning up data files — renaming away from member-specific names..."
[ -f dataset_memberB.csv ] && git mv dataset_memberB.csv data/dataset_raw_signature.csv
[ -f day3_results.csv ] && git mv day3_results.csv data/day3_results.csv

echo "Moving results files..."
[ -f eda_chart.png ] && git mv eda_chart.png results/eda_chart.png
[ -f final_comparison.csv ] && git mv final_comparison.csv results/final_comparison.csv
[ -f final_comparison_chart.png ] && git mv final_comparison_chart.png results/final_comparison_chart.png

echo "Moving roadmap PDF into docs/..."
[ -f "Quantum_AI_Crypto_4Day_Plan.pdf" ] && git mv "Quantum_AI_Crypto_4Day_Plan.pdf" docs/research_roadmap.pdf
[ -f "Quantum-Resistant_AI_Cryptography_-_Research_Roadmap.pdf" ] && git mv "Quantum-Resistant_AI_Cryptography_-_Research_Roadmap.pdf" docs/research_roadmap.pdf

echo ""
echo "Done. Review the new structure with: find . -type f -not -path './.git/*' | sort"
echo "Then fix imports inside the moved .py files (paths like 'data/dataset.csv' may need '../../data/dataset.csv')"
echo "Finally commit: git add -A && git commit -m 'Reorganize repo into professional structure'"