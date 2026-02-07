import pdfplumber

PDF_PATH = "KevinHuang_Resume2026.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    all_text = []
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        all_text.append(text)
        print(f"\n--- PAGE {i+1} ---\n")
        print(text[:2000])  # preview

full_text = "\n\n".join(all_text)

print("\n=== FULL TEXT LENGTH ===")
print(len(full_text))
