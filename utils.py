# import os
# import re
# import json
# import PyPDF2
# import requests
# from bs4 import BeautifulSoup
# from youtube_transcript_api import YouTubeTranscriptApi
# from PIL import Image
# # import pytesseract
# from typing import List, Dict, Any
# import hashlib

# def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 100) -> List[str]:
#     """Split text into overlapping chunks."""
#     chunks = []
#     start = 0
    
#     while start < len(text):
#         end = start + chunk_size
#         if end > len(text):
#             end = len(text)
        
#         # Try to split at sentence boundaries
#         if end < len(text):
#             # Look for sentence endings
#             sentence_end = max(text.rfind('. ', start, end),
#                              text.rfind('? ', start, end),
#                              text.rfind('! ', start, end))
            
#             if sentence_end != -1 and sentence_end > start + chunk_size // 2:
#                 end = sentence_end + 1
        
#         chunk = text[start:end].strip()
#         if chunk:
#             chunks.append(chunk)
        
#         start = end - chunk_overlap
#         if start <= 0:
#             break
    
#     return chunks

# # def extract_text_from_pdf(file_path: str) -> str:
# #     """Extract text from PDF file."""
# #     text = ""
# #     try:
# #         with open(file_path, 'rb') as file:
# #             reader = PyPDF2.PdfReader(file)
# #             for page in reader.pages:
# #                 text += page.extract_text() + "\n"
# #     except Exception as e:
# #         print(f"Error reading PDF {file_path}: {e}")
# #     return text

# def extract_text_from_pdf(file_path: str) -> str:
#     """Extract text from PDF file with better error handling."""
#     text = ""
#     try:
#         with open(file_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
            
#             # Check if PDF is encrypted
#             if reader.is_encrypted:
#                 print(f"PDF is encrypted: {file_path}")
#                 return ""
            
#             for page in reader.pages:
#                 page_text = page.extract_text()
#                 if page_text:
#                     text += page_text + "\n"
                
#     except PyPDF2.errors.PdfReadError as e:
#         print(f"PDF read error {file_path}: {e}")
#     except Exception as e:
#         print(f"Error reading PDF {file_path}: {e}")
    
#     return text

# def extract_text_from_website(url: str) -> str:
#     """Extract text from website."""
#     try:
#         response = requests.get(url, timeout=10)
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Remove unwanted elements
#         for element in soup(['script', 'style', 'nav', 'footer', 'header']):
#             element.decompose()
        
#         text = soup.get_text()
#         # Clean up text
#         lines = (line.strip() for line in text.splitlines())
#         chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
#         text = ' '.join(chunk for chunk in chunks if chunk)
#         return text
#     except Exception as e:
#         print(f"Error extracting text from {url}: {e}")
#         return ""

# def extract_transcript_from_youtube(video_url: str) -> str:
#     """Extract transcript from YouTube video."""
#     try:
#         video_id = video_url.split('v=')[-1].split('&')[0]
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         text = " ".join([entry['text'] for entry in transcript])
#         return text
#     except Exception as e:
#         print(f"Error extracting transcript from {video_url}: {e}")
#         return ""

# # def extract_text_from_image(image_path: str) -> str:
# #     """Extract text from image using OCR."""
# #     try:
# #         image = Image.open(image_path)
# #         text = pytesseract.image_to_string(image)
# #         return text
# #     except Exception as e:
# #         print(f"Error extracting text from image {image_path}: {e}")
# #         return ""

# def generate_document_id(content: str, source: str) -> str:
#     """Generate unique ID for document chunk."""
#     return hashlib.md5(f"{content}_{source}".encode()).hexdigest()

# def clean_text(text: str) -> str:
#     """Clean and normalize text."""
#     # Remove extra whitespace
#     text = re.sub(r'\s+', ' ', text)
#     # Remove non-printable characters
#     text = re.sub(r'[^\x20-\x7E\n\r]', '', text)
#     return text.strip()




import os
import re
import json
import PyPDF2
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from PIL import Image
# import pytesseract
from typing import List, Dict, Any
import hashlib

# def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 100) -> List[str]:
#     """Split text into overlapping chunks."""
#     chunks = []
#     start = 0
    
#     while start < len(text):
#         end = start + chunk_size
#         if end > len(text):
#             end = len(text)
        
#         # Try to split at sentence boundaries
#         if end < len(text):
#             # Look for sentence endings
#             sentence_end = max(text.rfind('. ', start, end),
#                              text.rfind('? ', start, end),
#                              text.rfind('! ', start, end))
            
#             if sentence_end != -1 and sentence_end > start + chunk_size // 2:
#                 end = sentence_end + 1
        
#         chunk = text[start:end].strip()
#         if chunk:
#             chunks.append(chunk)
        
#         start = end - chunk_overlap
#         if start <= 0:
#             break
    
#     return chunks

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file with comprehensive error handling."""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            # Use context manager for better resource handling
            reader = PyPDF2.PdfReader(file)
            
            # Check if PDF is encrypted
            if reader.is_encrypted:
                try:
                    # Try empty password decryption
                    reader.decrypt('')
                except:
                    print(f"PDF is encrypted and cannot be read: {file_path}")
                    return ""
            
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text += page_text + "\n"
                    else:
                        print(f"Page {page_num + 1} in {file_path} has no extractable text")
                except Exception as page_error:
                    print(f"Error extracting text from page {page_num + 1} in {file_path}: {page_error}")
                    continue
                
    except PyPDF2.errors.PdfReadError as e:
        print(f"PDF read error (corrupted file): {file_path}: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error reading PDF {file_path}: {e}")
        return ""
    
    return text

def extract_text_from_website(url: str) -> str:
    """Extract text from website."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Get text from main content areas
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if main_content:
            text = main_content.get_text()
        else:
            text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text
        
    except requests.RequestException as e:
        print(f"Network error extracting from {url}: {e}")
        return ""
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return ""

def extract_transcript_from_youtube(video_url: str) -> str:
    """Extract transcript from YouTube video."""
    try:
        # Extract video ID from various YouTube URL formats
        if 'youtube.com/watch?v=' in video_url:
            video_id = video_url.split('v=')[-1].split('&')[0]
        elif 'youtu.be/' in video_url:
            video_id = video_url.split('youtu.be/')[-1].split('?')[0]
        else:
            print(f"Invalid YouTube URL format: {video_url}")
            return ""
            
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text
        
    except Exception as e:
        print(f"Error extracting transcript from {video_url}: {e}")
        return ""

# def extract_text_from_image(image_path: str) -> str:
#     """Extract text from image using OCR."""
#     try:
#         image = Image.open(image_path)
#         text = pytesseract.image_to_string(image)
#         return text
#     except Exception as e:
#         print(f"Error extracting text from image {image_path}: {e}")
#         return ""

def generate_document_id(content: str, source: str) -> str:
    """Generate unique ID for document chunk."""
    return hashlib.md5(f"{content}_{source}".encode()).hexdigest()

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove non-printable characters (keep basic ASCII + newlines)
    text = re.sub(r'[^\x20-\x7E\n\r]', '', text)
    return text.strip()

# def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 100) -> List[str]:
#     """Split text into overlapping chunks with memory-efficient implementation."""
#     if not text or chunk_size <= 0:
#         return []
    
#     chunks = []
#     start = 0
#     text_length = len(text)
    
#     while start < text_length:
#         # Determine end position
#         end = min(start + chunk_size, text_length)
        
#         # Try to find a sentence boundary near the end
#         if end < text_length:
#             # Look for sentence endings in the last 100 characters of the chunk
#             boundary_chars = text[end - min(100, chunk_size//2):end + 50]
            
#             # Find the last sentence boundary
#             last_period = boundary_chars.rfind('. ')
#             last_question = boundary_chars.rfind('? ')
#             last_exclamation = boundary_chars.rfind('! ')
#             last_newline = boundary_chars.rfind('\n')
            
#             # Use the latest boundary found
#             boundary_pos = max(last_period, last_question, last_exclamation, last_newline)
            
#             if boundary_pos != -1:
#                 # Adjust boundary position relative to the full text
#                 boundary_pos += end - len(boundary_chars)
#                 if boundary_pos > start + chunk_size // 2:  # Only use if it's not too early
#                     end = boundary_pos + 1  # +1 to include the boundary character
        
#         # Extract the chunk
#         chunk = text[start:end].strip()
#         if chunk and len(chunk) >= 50:  # Only add meaningful chunks
#             chunks.append(chunk)
        
#         # Move to next position with overlap
#         start = end - chunk_overlap
#         if start < 0:
#             start = 0
#         if start >= text_length:
#             break
    
#     return chunks

def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks with memory-efficient implementation."""
    if not text or chunk_size <= 0:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    # Safety counter to prevent infinite loops
    safety_counter = 0
    max_iterations = 10000
    
    while start < text_length and safety_counter < max_iterations:
        safety_counter += 1
        
        # Determine end position
        end = min(start + chunk_size, text_length)
        
        # If we're at the end of the text, just take the remaining text
        if end == text_length:
            chunk = text[start:end].strip()
            if chunk and len(chunk) >= 50:
                chunks.append(chunk)
            break
        
        # Try to find a good breaking point near the end of the chunk
        lookahead_end = min(end + 100, text_length)  # Look ahead a bit
        segment = text[end:lookahead_end]
        
        # Find the first sentence ending after the chunk boundary
        period_pos = segment.find('. ')
        question_pos = segment.find('? ')
        exclamation_pos = segment.find('! ')
        newline_pos = segment.find('\n')
        
        # Find the earliest reasonable break point
        break_pos = -1
        for pos in [period_pos, question_pos, exclamation_pos, newline_pos]:
            if pos != -1 and (break_pos == -1 or pos < break_pos):
                break_pos = pos
        
        # If we found a break point, adjust the end position
        if break_pos != -1:
            end = end + break_pos + 1  # +1 to include the space or newline
        
        # Extract the chunk
        chunk = text[start:end].strip()
        if chunk and len(chunk) >= 50:  # Only add meaningful chunks
            chunks.append(chunk)
        
        # Move to next position with overlap
        start = max(end - chunk_overlap, start + chunk_size // 2)  # Ensure progress
        if start >= text_length:
            break
    
    return chunks

def safe_chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 100, max_chunks: int = 500) -> List[str]:
    """Safe version of chunk_text with memory protection."""
    try:
        # First try the main chunking method
        chunks = chunk_text(text, chunk_size, chunk_overlap)
        if chunks:
            return chunks[:max_chunks]
    except (MemoryError, RecursionError) as e:
        print(f"Chunking error ({type(e).__name__}) - using fallback method")
    
    # Fallback: simple splitting by sentences and paragraphs
    chunks = []
    
    # First split by double newlines (paragraphs)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    for paragraph in paragraphs:
        if len(paragraph) <= chunk_size:
            # If paragraph fits in one chunk, use it as is
            if paragraph and len(paragraph) >= 50:
                chunks.append(paragraph)
        else:
            # If paragraph is too long, split by sentences
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            current_chunk = ""
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                    
                if len(current_chunk) + len(sentence) + 1 < chunk_size:
                    current_chunk += " " + sentence if current_chunk else sentence
                else:
                    if current_chunk and len(current_chunk) >= 50:
                        chunks.append(current_chunk)
                    current_chunk = sentence
                    
                    if len(chunks) >= max_chunks:
                        break
            
            if current_chunk and len(current_chunk) >= 50 and len(chunks) < max_chunks:
                chunks.append(current_chunk)
        
        if len(chunks) >= max_chunks:
            break
    
    return chunks

def is_file_empty(file_path: str) -> bool:
    """Check if file is empty or contains only whitespace."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return not content.strip()
    except:
        return True