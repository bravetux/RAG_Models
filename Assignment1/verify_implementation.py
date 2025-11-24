import os
import sys
import time
from create_dummy_pdf import create_dummy_pdf
from summarize_pdf import load_and_split_pdf, setup_vectorstore, summarize_doc

def run_verification():
    print("Starting Verification Process...")
    results = []
    
    # 1. Check for PDF
    step_name = "PDF Generation"
    pdf_path = "verification_sample.pdf"
    print(f"Generating test PDF: {pdf_path}")
    try:
        create_dummy_pdf(pdf_path)
        if os.path.exists(pdf_path):
            print("PASS: PDF generated.")
            results.append({"step": step_name, "status": "PASS", "details": f"Created {pdf_path}"})
        else:
            print("FAIL: PDF generation failed.")
            results.append({"step": step_name, "status": "FAIL", "details": "File not found after generation attempt"})
    except Exception as e:
        results.append({"step": step_name, "status": "ERROR", "details": str(e)})

    # 2. Test Loading and Splitting
    step_name = "PDF Loading & Splitting"
    splits = []
    try:
        print("Testing PDF Loading and Splitting...")
        splits = load_and_split_pdf(pdf_path)
        if splits:
            print(f"PASS: PDF split into {len(splits)} chunks.")
            results.append({"step": step_name, "status": "PASS", "details": f"Created {len(splits)} chunks"})
        else:
            print("FAIL: No splits created.")
            results.append({"step": step_name, "status": "FAIL", "details": "No chunks returned"})
    except Exception as e:
        print(f"ERROR: {e}")
        results.append({"step": step_name, "status": "ERROR", "details": str(e)})

    # 3. Test Vector Store Creation
    step_name = "Vector Store Creation"
    vectorstore = None
    if splits:
        try:
            print("Testing Vector Store Creation (ChromaDB + Ollama)...")
            vectorstore = setup_vectorstore(splits)
            if vectorstore:
                print("PASS: Vector store created.")
                results.append({"step": step_name, "status": "PASS", "details": "ChromaDB initialized with Ollama embeddings"})
            else:
                print("FAIL: Vector store creation failed.")
                results.append({"step": step_name, "status": "FAIL", "details": "Vector store object is None"})
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({"step": step_name, "status": "ERROR", "details": str(e)})
    else:
        results.append({"step": step_name, "status": "SKIPPED", "details": "Skipped due to previous failure"})

    # 4. Test Summarization
    step_name = "Summarization"
    if vectorstore:
        try:
            print("Testing Summarization (Ollama LLM)...")
            summary = summarize_doc(vectorstore)
            
            if summary and len(summary) > 10:
                print("PASS: Summary generated successfully.")
                results.append({"step": step_name, "status": "PASS", "details": "Summary generated successfully"})
                print("-" * 20)
                print(f"Summary Preview: {summary[:100]}...")
                print("-" * 20)
            else:
                print(f"FAIL: Summary is too short or empty.")
                results.append({"step": step_name, "status": "FAIL", "details": f"Summary too short: {summary}"})
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({"step": step_name, "status": "ERROR", "details": str(e)})
    else:
        results.append({"step": step_name, "status": "SKIPPED", "details": "Skipped due to previous failure"})

    # Cleanup
    if os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
            print("Cleanup: Removed test PDF.")
        except:
            pass

    # Generate Report
    report_file = "verification_report.md"
    with open(report_file, "w") as f:
        f.write("# Verification Report\n\n")
        f.write(f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| Step | Status | Details |\n")
        f.write("| --- | --- | --- |\n")
        for res in results:
            icon = "[PASS]" if res["status"] == "PASS" else "[FAIL]" if res["status"] == "FAIL" else "[SKIP]" if res["status"] == "SKIPPED" else "[ERR ]"
            f.write(f"| {res['step']} | {icon} {res['status']} | {res['details']} |\n")
    
    print(f"\nReport generated at {report_file}")
    
    return all(r["status"] == "PASS" for r in results)

if __name__ == "__main__":
    success = run_verification()
    if not success:
        sys.exit(1)
