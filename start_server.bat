@echo off
echo =====================================================================
echo  DocuClassify AI - Production Document Classification System
echo =====================================================================
echo  Starting FastAPI Server on http://localhost:8000 ...
echo  (Serving both REST API and React 18 Frontend)
echo.
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
pause
