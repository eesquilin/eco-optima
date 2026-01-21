
[![Work in Progress](https://img.shields.io/badge/status-work--in--progress-orange?style=for-the-badge)](https://github.com/eesquilinv/eco-optima)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge)](https://www.python.org/)
[![Marimo](https://img.shields.io/badge/marimo-UI-green?style=for-the-badge)](https://marimo.io/)
[![LangChain](https://img.shields.io/badge/langchain-AI-yellow?style=for-the-badge)](https://python.langchain.com/)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-ML-red?style=for-the-badge)](https://scikit-learn.org/)

<p align="center">
  <img src="eco-optima-logo.png" alt="Eco-Optima Logo" width="200"/>
</p>

# Eco-Optima

> 🚧 **This project is a work in progress!** 🚧

## Purpose
Eco-Optima is an asset & compliance monitoring system for fuel tank anomaly detection. It leverages synthetic sensor data, machine learning, and agentic workflows to ensure regulatory compliance and operational safety.

## Technology Stack
- **Python 3.10+**
- **Marimo** (interactive UI)
- **Scikit-learn** (anomaly detection)
- **LangChain** (agentic workflow)
- **Google Generative AI** (Gemini)
- **Pandas & NumPy** (data processing)

## How to Start
1. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
2. **Set your Google API Key:**
	```bash
	export GOOGLE_API_KEY=your-key-here
	```
3. **Run the app:**
	```bash
	marimo run eco-optima.py
	```

## Features
- Synthetic fuel tank sensor data generation
- ML-based anomaly detection (Isolation Forest)
- Compliance rules loaded from text file
- Agentic workflow for professional work order generation
- Interactive UI with Marimo

---

<p align="center">
  <b>Eco-Optima &copy; 2026</b>
</p>