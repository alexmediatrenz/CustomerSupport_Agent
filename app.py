from flask import Flask, request, jsonify
from agent_config import agent

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle incoming chat requests."""
    try:
        data = request.get_json()
        if not data or 'message' not in data or 'conversation_id' not in data:
            return jsonify({'error': 'Invalid request: message and conversation_id are required'}), 400
        
        conversation_id = data['conversation_id']
        user_input = data['message'].strip()
        
        if not user_input:
            return jsonify({'response': 'Please provide a question or message.'}), 400
        
        # Get response from the agent
        response = agent.respond(user_input, conversation_id=conversation_id)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
