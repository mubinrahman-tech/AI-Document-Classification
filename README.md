# DocuClassify AI - Production-Quality AI-Based Document Classification System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/Frontend-React_18-61DAFB?style=flat-square&logo=react)](https://react.dev)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn)](https://scikit-learn.org)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

An intelligent, enterprise-grade web application that automatically ingests multi-format documents, extracts text with OCR fallbacks, cleans text using NLP preprocessing, predicts document categories using trained Machine Learning models (comparing Logistic Regression, Calibrated Linear SVM, and Multinomial Naive Bayes), and provides a modern SaaS productivity interface.

Designed and built for **B.Tech Artificial Intelligence and Data Science final-year projects**, internship demonstrations, and engineering portfolios.

---

## Key Features

1. **Multi-Format Document Ingestion**:
   - Drag-and-drop batch upload supporting **PDF, DOCX (Word), TXT, PPTX (PowerPoint), and JPG/PNG scanned images**.
   - Automated text extraction using **PyMuPDF**, **PyPDF**, **python-docx**, and **python-pptx**.
   - Optical Character Recognition (**OCR via Tesseract**) for scanned PDFs and image files with graceful host fallback.

2. **Machine Learning Pipeline**:
   - Sublinear **TF-IDF Bi-gram Vectorization** (`ngram_range=(1,2)`, `max_features=5000`).
   - Comparative evaluation of **Multinomial Naive Bayes**, **Linear SVM (Calibrated via Platt Scaling)**, and **Logistic Regression**.
   - Genuine test metrics: **Accuracy, Weighted Precision, Recall, and F1-Score**.
   - Model selection: Automated selection and persistence of the best-performing model via **Joblib**.
   - **Alternative Top-3 Predictions**: Displays full probability distribution spread for every prediction.
   - **Confidence Thresholding**: Configurable threshold (default 35%) automatically routes ambiguous or low-confidence files to *Other/Unclassified* for human audit.

3. **Human Feedback & Active Learning**:
   - Users can manually override and correct predicted categories.
   - Feedback notes and verification flags are saved to the SQLite database.
   - One-click model retraining pipeline (`POST /api/ml/retrain`) incorporates new data and recalculates genuine benchmark metrics.

4. **SaaS Productivity UI / UX**:
   - Modern dark navy and clean white theme inspired by Linear and modern AI platforms.
   - 7 Full-Featured Pages:
     1. **Dashboard**: High-level metrics, recent uploads, category mini-distribution, 1-click demo loader.
     2. **Upload Documents**: Drag-and-drop multi-file uploader with live extraction preview.
     3. **All Documents**: Document repository with search, category filtering pills, sorting, and pagination.
     4. **Classification Results**: Detailed probability analysis, top alternatives, and compliance advisory warnings.
     5. **Analytics**: Interactive **Chart.js** visualizations (Doughnut category distribution, Bar confidence buckets, Line ingestion velocity).
     6. **Model Performance**: Model comparison scorecard, interactive **Confusion Matrix heatmap**, per-class precision/recall breakdown, and an **Interactive Live Text Sandbox**.
     7. **Settings**: Confidence threshold slider, active model selector, OCR status, and demo reset.

5. **Instant Demonstration**:
   - Includes **9 Pre-Generated Multi-Format Sample Documents** across all categories.
   - One-click **"Load Demo Samples"** button populates the repository instantly for live presentations.

---

## Document Taxonomy (9 Target Categories)

| # | Category | Typical Document Types | Key Domain Signals |
|---|---|---|---|
| 1 | **Academic Documents** | Research papers, theses, citations, dissertations | `abstract`, `methodology`, `p-value`, `empirical`, `references` |
| 2 | **Financial Documents** | Invoices, balance sheets, tax returns, audits | `invoice`, `subtotal`, `tax`, `payable`, `balance sheet`, `ebitda` |
| 3 | **Legal Documents** | NDAs, master services agreements, lease deeds | `whereas`, `confidential`, `indemnification`, `governing law` |
| 4 | **Medical Documents** | Clinical discharge summaries, prescriptions | `diagnosis`, `mrn`, `rx`, `dosage`, `vital signs`, `icd-10` |
| 5 | **Business Documents** | Quarterly business reviews (QBR), pitch decks | `executive summary`, `kpi`, `arr`, `market opportunity`, `cac` |
| 6 | **Government Documents** | Official gazettes, passport forms, circulars | `gazette`, `statutory`, `pursuant to`, `ministry`, `notification` |
| 7 | **Technical Documents** | API specifications, architecture manuals, Dockerfiles | `endpoints`, `dockerfile`, `kubernetes`, `payload`, `latency` |
| 8 | **Personal Documents** | Resumes / CVs, cover letters, academic SOPs | `curriculum vitae`, `education`, `skills`, `experience`, `gpa` |
| 9 | **Other/Unclassified** | Miscellaneous notes, recipes, low-confidence text | Ambient text, ambiguous fragments, non-domain content |

---

## Project Structure

```
AI-DOCUMENT-CLASSIFICATION/
├── backend/
│   ├── app/
│   │   ├── config.py              # Application settings and paths
│   │   ├── database.py            # SQLite engine & SQLAlchemy session
│   │   ├── main.py                # FastAPI app & static file serving
│   │   ├── models/                # Database ORM models
│   │   │   └── document.py        # Document SQLAlchemy model
│   │   ├── schemas/               # Pydantic schemas for requests/responses
│   │   │   └── document.py
│   │   ├── services/
│   │   │   ├── text_extractor.py  # PyMuPDF, pypdf, docx, pptx, OCR
│   │   │   ├── preprocessor.py    # NLP cleaning, token stats, keywords
│   │   │   ├── classifier.py      # ML inference, top alternatives, threshold
│   │   │   └── sample_generator.py # Generates real multi-format sample files
│   │   └── routers/
│   │       ├── documents.py       # Ingest, query, correct, download, delete
│   │       ├── analytics.py       # Summary, category & confidence charts
│   │       ├── ml.py              # Model comparison, retrain, sandbox
│   │       └── settings.py        # Configuration & reset
│   └── static/                    # Built production React bundle
├── ml_model/
│   ├── dataset_generator.py       # Generates labeled corpus across 9 categories
│   ├── train.py                   # Trains & evaluates MNB, SVM, Logistic Regression
│   └── saved_models/              # Exported Joblib models, vectorizer & metrics
│       ├── best_model.joblib
│       ├── tfidf_vectorizer.joblib
│       ├── model_comparison.json  # Genuine computed metrics
│       └── metadata.json
├── dataset/
│   ├── document_classification_dataset.csv
│   └── categories.json
├── sample_docs/                   # Real multi-format sample files for testing
│   ├── Sample_Academic_Research_Paper.pdf
│   ├── Sample_Financial_Invoice_Statement.docx
│   ├── Sample_Legal_NonDisclosure_Agreement.pdf
│   ├── Sample_Medical_Clinical_Summary.txt
│   ├── Sample_Business_Executive_Review.pptx
│   ├── Sample_Technical_API_Architecture.txt
│   ├── Sample_Personal_Candidate_Resume.docx
│   ├── Sample_Government_Official_Gazette.pdf
│   └── Sample_Scanned_Prescription_Receipt.png
├── frontend/
│   ├── src/
│   │   ├── components/            # Sidebar, Navbar, Modals, Badges, Dropzone
│   │   ├── pages/                 # Dashboard, Upload, Documents, Analytics, etc.
│   │   ├── services/api.js        # Axios API client
│   │   └── utils/formatters.js
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── documentation/
│   ├── ARCHITECTURE.md            # Detailed system architecture
│   ├── API_REFERENCE.md           # REST API endpoint reference
│   └── ML_EVALUATION.md           # Model benchmarking & calibration
├── requirements.txt               # Python dependencies
├── start_server.bat               # 1-click startup (FastAPI + React bundle)
├── start_dev.bat                  # 1-click full-stack dev mode (FastAPI + Vite)
└── README.md
```

---

## Quick Start Guide

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** (for frontend development)

### Option 1: 1-Click Production Server (Recommended)
Double-click `start_server.bat` or run:
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!
The application serves both the backend REST API and the React single-page frontend.

### Option 2: Full-Stack Development Mode
Double-click `start_dev.bat` or run in two separate terminals:
```bash
# Terminal 1: Backend
python -m uvicorn backend.app.main:app --port 8000 --reload

# Terminal 2: Frontend (Vite with hot-reload)
cd frontend
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)**.

---

## How to Test the Complete Workflow

1. Open the web application at `http://localhost:8000`.
2. Click the **"Load Demo Samples"** button on the Navbar or Dashboard.
   - Ingests 9 multi-format sample documents (PDF, DOCX, TXT, PPTX, PNG).
3. Navigate to **All Documents**:
   - Filter by category, search by keywords, or sort by confidence.
   - Click on any document row to inspect the full extracted text, top alternative probabilities, and domain features.
4. Test **Category Correction**:
   - Click "Correct Category", select a different category, add notes, and save.
   - The badge updates immediately to `Verified` and the analytics dashboard updates the human feedback rate.
5. Navigate to **Upload Documents**:
   - Drag and drop your own `.pdf`, `.docx`, `.txt`, `.pptx`, or `.jpg`/`.png` files.
   - Watch the instant text extraction and classification.
6. Navigate to **Analytics**:
   - Inspect the interactive Doughnut category distribution, confidence histogram, and ingestion velocity timeline.
7. Navigate to **Model Performance**:
   - Review the comparative scorecard (Accuracy, Precision, Recall, F1) across Logistic Regression, Linear SVM, and Naive Bayes.
   - Inspect the **Confusion Matrix Heatmap**.
   - Use the **Live Interactive Sandbox**: paste any paragraph and click "Classify Text" to observe real-time classification and keyword signals!

---

## Academic / Viva Discussion Points

1. **Why TF-IDF + Calibrated Linear Classifiers over Large Language Models (LLMs)?**
   - For enterprise document categorization, sublinear TF-IDF + Calibrated Linear Classifiers provide sub-50ms deterministic inference, zero GPU requirements, no API token costs, and 100% data privacy without sending sensitive enterprise documents over external networks.
2. **How are Probabilities Obtained from Linear SVMs?**
   - Standard Linear SVMs produce decision boundary distances rather than probabilities. We employ `CalibratedClassifierCV` using Platt scaling (sigmoid fitting via cross-validation) to transform uncalibrated SVM margins into well-calibrated probabilities suitable for multi-class ranking.
3. **How Does the System Handle Low-Information or Scanned Files?**
   - If extracted text is sparse (< 30 characters), the pipeline flags the file, attempts OCR via Tesseract, and checks confidence against the minimum threshold ($\theta = 0.35$). If confidence is below threshold, it routes the file to `Other/Unclassified` to prevent false positive classifications.

---

## License
MIT License. Built for academic, demonstration, and production deployment.
