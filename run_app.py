# import os
# import sys
# from app import app

# if __name__ == "__main__":
#     # Disable problematic console output on Windows
#     if os.name == 'nt':  # Windows
#         import warnings
#         warnings.filterwarnings("ignore")
        
#     print("🔍 Starting Cyber-Forensics RAG System...")
#     print("🌐 Server will be available at: http://localhost:5000")
#     print("⚡ Press Ctrl+C to stop the server")
    
#     # Run without debug mode to avoid console issues
#     app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)

from app import app
from waitress import serve
import os

print("🔍 Starting Cyber-Forensics RAG System with Waitress...")
print("🌐 Server: http://localhost:5000")
print("⚡ Press Ctrl+C to stop")

# Use Waitress instead of Flask dev server
serve(app, host='0.0.0.0', port=5000)