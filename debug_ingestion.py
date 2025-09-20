from utils import extract_text_from_pdf, safe_chunk_text, clean_text , chunk_text
from config import Config

def test_pdf_processing(pdf_path):
    print(f"Testing PDF: {pdf_path}")
    
    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_path)
    print(f"1. Text extracted: {len(text)} characters")
    
    # Step 2: Clean text
    cleaned_text = clean_text(text)
    print(f"2. Text cleaned: {len(cleaned_text)} characters")
    
    # Step 3: Chunk text
    chunks = chunk_text(cleaned_text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
    print(f"3. Chunks created: {len(chunks)} chunks")
    
    # Show first chunk
    if chunks:
        print(f"First chunk ({len(chunks[0])} chars):")
        print(chunks[0][:200] + "...")
    
    return chunks

# Test the problematic PDF
pdf_path = "./data/documents/150874.pdf"
chunks = test_pdf_processing(pdf_path)