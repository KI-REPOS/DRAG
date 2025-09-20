from flask import Flask, render_template, request, jsonify, send_file
from rag_pipeline import RAGPipeline
from datetime import datetime
import json
import os
from config import Config

app = Flask(__name__)
rag_pipeline = RAGPipeline()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        response, sources = rag_pipeline.query(question)
        
        return jsonify({
            'response': response,
            'sources': sources,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    try:
        rag_pipeline.clear_conversation()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_conversation():
    try:
        data = request.get_json()
        conversation = data.get('conversation', [])
        
        # Create export content
        export_content = "Cyber-Forensics Q&A Export\n"
        export_content += "=" * 40 + "\n\n"
        
        for msg in conversation:
            export_content += f"{msg['role'].upper()}: {msg['content']}\n"
            if 'sources' in msg and msg['sources']:
                export_content += "Sources:\n"
                for source in msg['sources']:
                    export_content += f"  - {source['source']} (Chunk {source['chunk_index']})\n"
            export_content += f"Timestamp: {msg.get('timestamp', 'N/A')}\n"
            export_content += "-" * 40 + "\n"
        
        # Save to temporary file
        filename = f"forensics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join('/tmp', filename)
        
        with open(filepath, 'w') as f:
            f.write(export_content)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)