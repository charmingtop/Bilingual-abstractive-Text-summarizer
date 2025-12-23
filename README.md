Abstractive Text Summarizer with Translation

(BART-Large CNN Model)

📌 Project Overview

This project implements an abstractive text summarization system using Facebook’s BART-Large CNN model, a transformer-based sequence-to-sequence architecture trained on the CNN/DailyMail dataset.

The system supports Hindi input text by first translating it to English using the Google Translate API, after which summarization is performed. This enables effective multilingual summarization, particularly for Hindi-to-English workflows.

The project also provides an interactive summarization interface, logging, configuration via YAML, and batch execution support.

✨ Key Features

Abstractive summarization using BART-Large CNN

Hindi → English translation using Google Translate API

Interactive command-line summarizer

Configurable parameters via config.yaml

Logging support (summarizer.log)

Modular and extensible Python codebase

Windows batch execution support

🧠 Model Information

Model: facebook/bart-large-cnn

Architecture: Transformer (Encoder–Decoder)

Training Data: CNN / DailyMail

Summarization Type: Abstractive

The model generates summaries by understanding semantic meaning and context, producing fluent and human-like summaries rather than extracting sentences verbatim.

🌐 Translation Pipeline

Source Language: Hindi

Target Language: English

Service: Google Translate API

Workflow:

Hindi text is translated to English

Translated text is passed to the BART summarizer

Abstractive summary is generated in English

📁 Project Structure
project/
│── __pycache__/                 # Python cache (ignored)
│── .venv/                       # Virtual environment (ignored)
│── examples/                    # Sample input texts
│── tests/                       # Test cases
│── text_summariser.py           # Core summarization logic
│── interactive_summarizer.py    # Interactive CLI-based summarizer
│── interactive_summarizer_withhindi.py  # Hindi interactive version
│── simpler.py                   # Simplified summarization script
│── summarizer.py                # BART model wrapper
│── config.yaml                  # Configuration parameters
│── requirements.txt             # Python dependencies
│── run_summarizer.bat           # Windows batch runner
│── summarizer.log               # Execution logs
│── .gitignore                   # Git ignore rules
│── README.md                    # Project documentation

⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/<your-username>/summariser.git
cd summariser

2. Create and activate virtual environment
python -m venv .venv


Windows

.venv\Scripts\activate


Linux / macOS

source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

▶️ Usage
Interactive Mode
python interactive_summarizer.py

Simplified Execution
python simpler.py

Windows Batch Execution
run_summarizer.bat


Follow the prompts to:

Enter or load text

Translate Hindi input (if applicable)

Generate an abstractive summary

⚙️ Configuration

Project parameters can be modified using:

config.yaml


This includes:

Summary length

Chunk size

Translation options

Logging settings

📦 Dependencies

Key libraries used:

transformers

torch

nltk

tqdm

googletrans / Google Translate API client

pyyaml

All dependencies are listed in requirements.txt.

🚀 Applications

News article summarization

Academic document summarization

Hindi-to-English NLP workflows

AI / NLP learning projects

College-level major / mini projects

⚠️ Limitations

Token length limited by BART model constraints

Output summary is generated only in English

Translation accuracy depends on external API quality

🔮 Future Enhancements

English → Hindi summary translation

Support for additional Indian languages

Web-based interface (Flask / FastAPI)

Fine-tuned domain-specific summarization

👤 Author

Omesh Singh
AI & NLP Enthusiast
Bachelor’s Student

📜 License

This project is developed for educational and academic purposes.
