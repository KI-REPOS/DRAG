from utils import extract_text_from_pdf

# Test PDF extraction
pdf_path = "./data/documents/150874.pdf"
text = extract_text_from_pdf(pdf_path)

print(f"Extracted text length: {len(text)}")
print("First 500 characters:")
print(text[:500])