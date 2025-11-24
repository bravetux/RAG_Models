@echo off
echo ==========================================
echo      RAG PDF Summarizer Launcher
echo ==========================================

echo.
echo Select an option:
echo 1. Run Summarizer (Default: sample.pdf)
echo 2. Run Verification (Generates Report)
echo 3. Exit
echo.

set /p choice="Enter choice (1/2/3): "

if "%choice%"=="1" goto run_app
if "%choice%"=="2" goto run_verify
if "%choice%"=="3" goto end

:run_app
echo.
set /p pdf_file="Enter PDF filename (default: sample.pdf): "
if "%pdf_file%"=="" set pdf_file=sample.pdf

if not exist "%pdf_file%" (
    echo.
    echo File %pdf_file% not found!
    echo Generating dummy PDF...
    python create_dummy_pdf.py
)

echo.
echo Running summarization on %pdf_file%...
python summarize_pdf.py "%pdf_file%"
goto end

:run_verify
echo.
echo Running verification script...
python verify_implementation.py
echo.
if exist verification_report.md (
    echo Report generated: verification_report.md
    type verification_report.md
)
goto end

:end
echo.
echo Done.
pause
