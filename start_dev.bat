@echo off
echo =====================================================================
echo  DocuClassify AI - Full Stack Development Mode
echo =====================================================================
echo  1. Starting Backend API at http://localhost:8000 ...
start cmd /k "python -m uvicorn backend.app.main:app --port 8000 --reload"
echo.
echo  2. Starting Vite React Frontend at http://localhost:5173 ...
cd frontend
npm run dev
