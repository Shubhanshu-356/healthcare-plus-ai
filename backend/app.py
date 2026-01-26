from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os
import numpy as np
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app)

# ==========================================
# 🧠 AI MODEL INITIALIZATION
# ==========================================
print("⏳ Loading AI Model... (This might take a moment)")
# We use 'all-MiniLM-L6-v2'. It's small, fast, and perfect for semantic search.
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ AI Model Loaded!")

# ==========================================
# FILE SETUP
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATIENT_DATA_FILE = os.path.join(BASE_DIR, 'patient_submissions.json')
VOLUNTEER_DATA_FILE = os.path.join(BASE_DIR, 'volunteer_submissions.json')

# ==========================================
# ADVANCED FAQ DATABASE (With 'Questions' for AI matching)
# ==========================================
# We added 'questions' list to each entry. The AI will compare user input against these.
FAQ_DATABASE = [
    {
        "id": 1,
        "questions": ["When are you open?", "What are your hours?", "Can I come in today?", "timing"],
        "answer": "Our clinic is open Monday-Friday, 9 AM to 6 PM. Same-day appointments are available for urgent cases."
    },
    {
        "id": 2,
        "questions": ["I have an emergency", "I am dying", "Need ambulance", "critical condition", "urgent help"],
        "answer": "For medical emergencies, please call 911 immediately. Our emergency hotline is available 24/7 at +1-234-567-8999."
    },
    {
        "id": 3,
        "questions": ["Do you take insurance?", "How much does it cost?", "payment options", "fees"],
        "answer": "We accept Medicare, Medicaid, and most major insurance. We also offer sliding scale fees for uninsured patients."
    },
    {
        "id": 4,
        "questions": ["I want to volunteer", "How can I help?", "Join the team", "jobs"],
        "answer": "We need volunteers! Please use the 'Volunteer' tab above to fill out the registration form."
    },
    {
        "id": 5,
        "questions": ["Do you have heart doctors?", "pediatrician available?", "specialists", "doctors list"],
        "answer": "Yes, we have specialists in Cardiology, Pediatrics, and Orthopedics. You can view profiles on our main website."
    },
    {
        "id": 6,
        "questions": ["refill prescription", "need medicine", "pharmacy hours", "drugs"],
        "answer": "Our in-house pharmacy is open during clinic hours. Call 24 hours in advance for refills."
    },
    {
        "id": 7,
        "questions": ["covid test", "vaccine", "corona virus", "symptoms of covid"],
        "answer": "We offer free COVID-19 testing for symptomatic patients. Vaccines require an appointment."
    }
]

# PRE-COMPUTE EMBEDDINGS (This makes the chatbot super fast)
# We convert all FAQ questions into numbers (vectors) once when the server starts.
faq_questions = []
faq_answers = []
for entry in FAQ_DATABASE:
    for q in entry['questions']:
        faq_questions.append(q)
        faq_answers.append(entry['answer'])

# Convert questions to vectors
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def analyze_urgency(message):
    """
    Simple keyword-based sentiment analysis for Triage.
    Returns: Priority Level (Low, Medium, High)
    """
    urgent_words = ['pain', 'blood', 'emergency', 'severe', 'chest', 'difficulty', 'breathing']
    medium_words = ['fever', 'cold', 'sick', 'appointment', 'schedule', 'refill']
    
    message = message.lower()
    if any(word in message for word in urgent_words):
        return "HIGH PRIORITY 🔴"
    elif any(word in message for word in medium_words):
        return "MEDIUM PRIORITY 🟡"
    return "Standard Priority 🟢"

# ==========================================
# ROUTES
# ==========================================

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """AI Semantic Search Chatbot"""
    data = request.json
    query = data.get('query', '')
    
    # Encode user query to vector
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # Calculate Similarity (Cosine Similarity)
    # This compares the angle between the user's thought and our FAQ thoughts
    cos_scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    
    # Find the best match
    best_match_index = int(np.argmax(cos_scores))
    best_score = float(cos_scores[best_match_index])
    
    print(f"🧠 Query: '{query}' | Match: '{faq_questions[best_match_index]}' | Score: {best_score}")

    # Threshold: If similarity is too low (e.g. < 0.3), the AI is confused
    if best_score < 0.35:
        return jsonify({
            "success": True,
            "answer": "I'm not sure I understand. Could you rephrase that? Or contact support at +1-234-567-8900."
        })
    
    return jsonify({
        "success": True,
        "answer": faq_answers[best_match_index]
    })

@app.route('/api/patient-support', methods=['POST'])
def patient_support():
    try:
        data = request.json
        required = ['name', 'email', 'phone', 'message']
        if not all(k in data for k in required):
            return jsonify({"success": False, "error": "Missing fields"}), 400
        
        # 🚀 INNOVATION: Auto-Triage System
        priority = analyze_urgency(data['message'])
        
        current_data = load_data(PATIENT_DATA_FILE)
        submission = {
            "id": len(current_data) + 1,
            "timestamp": datetime.now().isoformat(),
            "priority": priority, # Saving the AI analysis
            **data
        }
        current_data.append(submission)
        save_data(PATIENT_DATA_FILE, current_data)
        
        # We return the priority to the frontend to show the user
        return jsonify({
            "success": True,
            "message": "Request Received",
            "auto_response": f"Thank you, {data['name']}. Based on your message, we have flagged this as {priority}. A nurse will contact you shortly."
        }), 201
        
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/volunteer-registration', methods=['POST'])
def volunteer_registration():
    # (Keep your existing logic here, it is fine)
    try:
        data = request.json
        current_data = load_data(VOLUNTEER_DATA_FILE)
        submission = {
            "id": len(current_data) + 1,
            "timestamp": datetime.now().isoformat(),
            **data
        }
        current_data.append(submission)
        save_data(VOLUNTEER_DATA_FILE, current_data)
        return jsonify({"success": True, "message": "Registered!"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# NEW: DATA SUMMARY ENDPOINT (Innovation Requirement)
@app.route('/api/admin/summary', methods=['GET'])
def get_summary():
    patients = load_data(PATIENT_DATA_FILE)
    volunteers = load_data(VOLUNTEER_DATA_FILE)
    
    # Calculate basic stats
    total_patients = len(patients)
    high_priority = sum(1 for p in patients if "HIGH" in p.get('priority', ''))
    
    return jsonify({
        "total_patients": total_patients,
        "urgent_cases": high_priority,
        "total_volunteers": len(volunteers),
        "status": "Healthy"
    })

# ... (All your upper code stays the same) ...

if __name__ == '__main__':
    # Ensure data files exist (Cloud storage is temporary, but this prevents crashes)
    if not os.path.exists(PATIENT_DATA_FILE): save_data(PATIENT_DATA_FILE, [])
    if not os.path.exists(VOLUNTEER_DATA_FILE): save_data(VOLUNTEER_DATA_FILE, [])
    
    print("🏥 AI Healthcare Server Running...")
    
    # ☁️ CLOUD FIX: Get the PORT from the cloud environment (Render gives this automatically)
    port = int(os.environ.get('PORT', 5000))
    # ☁️ CLOUD FIX: Bind to '0.0.0.0' so the cloud can see your app
    app.run(host='0.0.0.0', port=port)