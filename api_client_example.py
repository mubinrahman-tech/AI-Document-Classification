"""
DocuClassify AI - Python API Client Example
Demonstrates how to interact with the Document Classification API programmatically:
1. Health check
2. Live raw text classification (no file needed)
3. Document file upload & classification (PDF, DOCX, TXT, PPTX, Images)
4. Querying classified documents with filters
5. Human feedback / Category correction
6. Model benchmark & metrics inspection
"""

import requests
import json
import os

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_api():
    # 1. Health Check
    print_section("1. Health Check")
    try:
        res = requests.get(f"{BASE_URL}/health")
        print("Status:", res.status_code)
        print("Response:", json.dumps(res.json(), indent=2))
    except requests.exceptions.ConnectionError:
        print(f"Error: Server not running. Start it with: python -m uvicorn backend.app.main:app --port 8000")
        return

    # 2. Live Text Prediction (No file upload needed)
    print_section("2. Live Text Classification (POST /api/ml/predict-text)")
    text_sample = (
        "CLINICAL DISCHARGE NOTE: Patient admitted with hypertensive crisis and acute chest pain. "
        "Diagnosed with NSTEMI (ICD-10: I21.4). Prescribed Aspirin 81mg, Metoprolol 25mg twice daily, "
        "and Atorvastatin 80mg at bedtime. Follow up with Dr. Hayes in Cardiology clinic."
    )
    payload = {
        "text": text_sample,
        "model_name": "Multinomial Naive Bayes"
    }
    res = requests.post(f"{BASE_URL}/ml/predict-text", json=payload)
    print("Input Text:", text_sample[:80] + "...")
    print("Predicted Category:", res.json().get("predicted_category"))
    print("Confidence Score:", f"{res.json().get('confidence_score') * 100:.1f}%")
    print("Alternative Predictions:")
    for alt in res.json().get("alternative_predictions", [])[:3]:
        print(f"  - {alt['category']}: {alt['percentage']}%")
    print("Detected Keywords:", res.json().get("top_matched_keywords"))

    # 3. Document File Upload & Classification
    print_section("3. Upload Document File (POST /api/documents/upload)")
    sample_pdf = os.path.join("sample_docs", "Sample_Legal_NonDisclosure_Agreement.pdf")
    if os.path.exists(sample_pdf):
        with open(sample_pdf, "rb") as f:
            files = [("files", ("Sample_Legal_NonDisclosure_Agreement.pdf", f, "application/pdf"))]
            res = requests.post(f"{BASE_URL}/documents/upload", files=files)
            print("Status:", res.status_code)
            uploaded_docs = res.json()
            doc = uploaded_docs[0]
            print(f"Uploaded: {doc['original_filename']}")
            print(f"Category: {doc['predicted_category']}")
            print(f"Confidence: {doc['confidence_score'] * 100:.1f}%")
            print(f"Words Extracted: {doc['word_count']}")
            doc_id = doc["id"]
    else:
        print("Sample PDF not found locally.")
        doc_id = None

    # 4. Get Documents List with Filter
    print_section("4. Query Documents (GET /api/documents?category=...)")
    res = requests.get(f"{BASE_URL}/documents", params={"limit": 5, "sort_by": "created_at", "sort_order": "desc"})
    data = res.json()
    print(f"Total in Database: {data['total']}")
    for d in data.get("documents", []):
        print(f"  [{d['id']}] {d['original_filename'][:35]:35} | {d['final_category']:22} | {d['confidence_score']*100:.1f}%")

    # 5. Correct Document Category (Human-in-the-Loop Feedback)
    if doc_id:
        print_section("5. Manual Category Correction (PATCH /api/documents/{id}/correct)")
        feedback = {
            "corrected_category": "Legal Documents",
            "notes": "Verified by legal compliance team via API."
        }
        res = requests.patch(f"{BASE_URL}/documents/{doc_id}/correct", json=feedback)
        print("Updated Document:")
        print(f"  ID: {res.json().get('id')}")
        print(f"  Final Category: {res.json().get('final_category')}")
        print(f"  Is User Corrected: {res.json().get('is_user_corrected')}")

    # 6. ML Model Scorecard
    print_section("6. ML Models Benchmark (GET /api/ml/models)")
    res = requests.get(f"{BASE_URL}/ml/models")
    ml_info = res.json()
    print("Active Model:", ml_info.get("active_model"))
    print("Model Comparison Scorecard:")
    for name, m in ml_info.get("models", {}).items():
        best_tag = " (BEST)" if m.get("is_best") else ""
        print(f"  - {name:25}: Accuracy={m['accuracy']*100:.1f}%, F1-Score={m['f1_weighted']*100:.1f}%, Training Time={m['training_time_sec']}s{best_tag}")

if __name__ == "__main__":
    test_api()
