from flask import Flask, render_template, request, jsonify
from enhancer import get_text_enhancer
from database import get_db_handler
import config
import time

app = Flask(__name__, static_url_path='/static')
enhancer = get_text_enhancer()
db = get_db_handler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance', methods=['POST'])
def enhance_text():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    input_text = data['text']
    
    # Remove artificial delay if you want accurate timing
    # time.sleep(1)  
    
    try:
        # Unpack result
        enhanced_text, duration = enhancer.enhance_text(input_text)
        
        # Log the interaction
        db.log_interaction(
            original_text=input_text,
            enhanced_text=enhanced_text,
            model_name=enhancer.model_name,
            user_feedback=None
        )
        
        # Return both text and duration
        return jsonify({'enhanced_text': enhanced_text, 'duration': duration})
    except Exception as e:
        # Return None for duration in case of error
        return jsonify({'error': str(e), 'duration': None}), 500

@app.route('/feedback', methods=['POST'])
def record_feedback():
    data = request.get_json()
    
    if not data or 'feedback' not in data or 'interactionId' not in data:
        return jsonify({'error': 'Invalid feedback data'}), 400
    
    # Here you would update the MongoDB record with the feedback
    # This is a placeholder for actual feedback implementation
    
    return jsonify({'success': True})

def run_webapp(debug=False, port=5000):
    app.run(debug=debug, port=port)

if __name__ == '__main__':
    run_webapp(debug=True)
