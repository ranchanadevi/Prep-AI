from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session
from models import db
from models.chat_history import ChatHistory
from utils.gemini_helper import GeminiHelper
from routes.auth import login_required

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@chatbot_bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    
    # Initialize session start time if not present
    if 'chat_session_start' not in session:
        session['chat_session_start'] = datetime.utcnow().isoformat()
        
    session_start = datetime.fromisoformat(session['chat_session_start'])
    
    # Fetch only chat history from the current active session
    chats = ChatHistory.query.filter(
        ChatHistory.user_id == user_id,
        ChatHistory.created_at >= session_start
    ).order_by(ChatHistory.created_at.asc()).all()
    
    return render_template('chatbot.html', chats=chats)

@chatbot_bp.route('/send', methods=['POST'])
@login_required
def send():
    user_id = session['user_id']
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'status': 'error', 'message': 'Empty message'}), 400

    # Retrieve recent chat history context for Gemini (up to last 10 exchanges)
    session_start = datetime.fromisoformat(session.get('chat_session_start', datetime.utcnow().isoformat()))
    history_records = ChatHistory.query.filter(
        ChatHistory.user_id == user_id,
        ChatHistory.created_at >= session_start
    ).order_by(ChatHistory.created_at.desc()).limit(10).all()
    
    # Format history as a list of dicts in ascending chronological order
    history = []
    for h in reversed(history_records):
        history.append({
            'message': h.message,
            'response': h.response
        })

    # Call Gemini helper with the prompt and session history
    ai_response = GeminiHelper.get_chat_response(message, history)
    
    # Save the interaction to the database
    new_chat = ChatHistory(
        user_id=user_id,
        message=message,
        response=ai_response
    )
    
    try:
        db.session.add(new_chat)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'response': ai_response
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error saving chat history: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to save conversation record.'
        }), 500

@chatbot_bp.route('/clear', methods=['POST'])
@login_required
def clear():
    # Update session start time to now.
    # This hides previous chat bubbles from the user and stops sending them as context,
    # but does NOT delete the actual database rows.
    session['chat_session_start'] = datetime.utcnow().isoformat()
    return jsonify({'status': 'success'})
