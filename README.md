# 🛡️ HSE-Guardian: Agentic AI for Industrial Safety

![Project Status](https://img.shields.io/badge/Status-Prototype-green) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![AI](https://img.shields.io/badge/Tech-YOLO11%20%7C%20Llama3%20%7C%20RAG-orange)

**HSE-Guardian** is an autonomous industrial safety monitoring system designed for the Oil & Gas sector. It integrates **Computer Vision**, **Retrieval-Augmented Generation (RAG)**, and **Agentic Workflow** to detect, analyze, and report Health, Safety, and Environment (HSE) violations in real-time.

Unlike traditional CCTV monitoring, HSE-Guardian acts as an **Intelligent Agent** that understands specific company Standard Operating Procedures (SOPs) and generates automated legal compliance reports.

## 🧠 Key Capabilities

### 1. 👁️ Intelligent Vision (Perception Layer)
- Powered by **YOLO11** (Fine-tuned) for real-time PPE detection.
- Capable of detecting **Multi-Class Violations** simultaneously (e.g., Missing Hardhat + Missing Mask).
- Engineered for high-speed inference on edge devices.

### 2. 🤖 Agentic Reasoning (Cognitive Layer)
- Implements an **Agentic AI Workflow** using **Llama-3 (via Groq)**.
- **Context-Aware Analysis:** Utilizes **RAG** to fetch specific clauses from the internal Company SOP (PDF/Txt) instead of generic safety rules.
- **Autonomous Decision Making:** The agent automatically determines the severity level (Low/Medium/High) and appropriate sanctions based on the detected violation context.

### 3. 📊 Predictive Analytics (Insight Layer)
- **Real-time Command Center** built with **Streamlit**.
- Features an **Early Warning System (EWS)** that analyzes historical logs to predict high-risk zones and fatigue-related incidents during night shifts.
- Provides actionable insights for HSE Managers to perform preventive inspections.

---

## 🏗️ System Architecture

The system follows a modular **Event-Driven Architecture**:

```mermaid
graph LR
    A[CCTV Feed] -->|Frame| B(YOLOv11 Detector)
    B -->|Violation Detected| C{Agentic Controller}
    C -->|Context Retrieval| D[RAG Engine / SOP Database]
    D -->|Prompt Engineering| E[LLM Inference]
    E -->|Structured Report| F[(CSV/SQL Database)]
    F -->|Real-time Data| G[Streamlit Dashboard]
