# Sentence Autocomplete

AI-powered sentence completion system inspired by Gmail Smart Compose. Type an incomplete sentence, press Space for suggestions, Tab to accept.

## Introduction

**Sentence Autocomplete** provides real-time text suggestions using deep learning. Built with Flask backend and modern HTML/JavaScript frontend for seamless UX.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser
# http://localhost:8000
```

## Techniques & Libraries

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Model** | GPT-2 (Hugging Face) | Pre-trained language model for text generation |
| **Backend** | Flask | REST API server |
| **Frontend** | HTML/CSS/JavaScript | Interactive web UI |
| **Deep Learning** | PyTorch | Neural network framework |

### Sampling Techniques

- **Top-k Sampling**: Sample from top k most probable tokens → Reduces unlikely outputs
- **Top-p (Nucleus) Sampling**: Sample from smallest set with cumulative prob ≥ p → Better diversity
- **Temperature Control**: Adjust randomness (0=deterministic, 2=creative)

### Streamlit UI
<img width="1756" height="953" alt="Screenshot 2025-12-06 at 6 04 41 PM" src="https://github.com/user-attachments/assets/de495a11-c742-467e-886b-28925e7f87e3" />

