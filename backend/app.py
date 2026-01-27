from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# ==========================================
# 🧠 CONFIGURATION
# =========================================
print("⏳ Loading Model...")
vectorizer = TfidfVectorizer()

# ==========================================
# 📂 FILE STORAGE SETUP
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATIENT_FILE = os.path.join(BASE_DIR, 'patient_submissions.json')
VOLUNTEER_FILE = os.path.join(BASE_DIR, 'volunteer_submissions.json')

# ==========================================
# 📚 THE KNOWLEDGE BASE (FAQ Database)
# ==========================================
FAQ_DATABASE = [
    # --- EMERGENCY ---
    {
        "id": 1,
        "questions": ["I have an emergency", "dying", "ambulance", "911", "chest pain", "bleeding", "stroke", "heart attack", "unconscious", "poison", "suicide", "broken bone", "difficulty breathing"],
        "answer": "🚨 MEDICAL EMERGENCY: Please call 911 immediately or go to the nearest Emergency Room. Our emergency hotline is available 24/7 at +1-234-567-8999."
    },
    # --- HOURS & LOCATION ---
    {
        "id": 2,
        "questions": ["When are you open?", "hours", "timing", "schedule", "open", "close", "weekends", "working days", "holiday hours"],
        "answer": "Our clinic is open Monday-Friday, 9 AM to 6 PM, and Saturdays 10 AM to 2 PM. We are closed on Sundays."
    },
    {
        "id": 3,
        "questions": ["where are you located?", "address", "location", "directions", "map", "gps", "street", "how to reach"],
        "answer": "We are located at 123 Healthcare Blvd, New York, NY 10001. We are right next to the Central Park Metro Station."
    },
    {
        "id": 4,
        "questions": ["parking", "garage", "where to park", "parking fee", "valet", "car"],
        "answer": "We have a dedicated patient parking garage behind the building. Parking is free for the first 2 hours with validation."
    },
    # --- APPOINTMENTS ---
    {
        "id": 5,
        "questions": ["book appointment", "schedule visit", "see a doctor", "make an appointment", "reservation", "booking", "slot"],
        "answer": "You can book an appointment online via our 'Appointments' tab, or call our front desk at +1-234-567-8900."
    },
    {
        "id": 6,
        "questions": ["cancel appointment", "reschedule", "change time", "cannot make it", "missed appointment", "late", "cancel booking"],
        "answer": "To cancel or reschedule, please call us 24 hours in advance to avoid a cancellation fee. You can also manage bookings in the Patient Portal."
    },
    {
        "id": 7,
        "questions": ["walk in", "no appointment", "urgent care", "can I just walk in?", "without appointment", "same day", "fever", "cough", "cold", "flu", "sick", "headache"],
        "answer": "For symptoms like fever or flu, we accept walk-ins for Urgent Care between 9 AM and 4 PM. Please wear a mask."
    },
    # --- BILLING & INSURANCE ---
    {
        "id": 8,
        "questions": ["Do you take insurance?", "cost", "payment options", "fees", "bill", "price", "charges", "money", "pay", "credit card", "medicare", "medicaid"],
        "answer": "We accept Medicare, Medicaid, and most major private insurance plans. We also accept cash, credit cards, and Apple Pay."
    },
    {
        "id": 9,
        "questions": ["pay bill", "billing department", "invoice", "statement", "owe money", "balance", "online payment"],
        "answer": "You can pay your bill online through the Patient Portal using your Invoice ID. For billing questions, call extension #4."
    },
    # --- SERVICES ---
    {
        "id": 10,
        "questions": ["covid test", "vaccine", "corona virus", "symptoms of covid", "flu shot", "vaccination", "testing", "pcr", "rapid test"],
        "answer": "We offer PCR and Rapid COVID-19 testing. Walk-ins are accepted for testing. Vaccines (Covid/Flu) require an appointment."
    },
    {
        "id": 11,
        "questions": ["refill prescription", "need medicine", "pharmacy hours", "drugs", "medication", "pills", "tablet", "pharmacy", "rx"],
        "answer": "Our pharmacy is open 9 AM - 6 PM. You can request refills via the app or by calling the pharmacy directly at extension #2."
    },
    {
        "id": 12,
        "questions": ["blood test", "lab results", "xray", "mri", "scan", "radiology", "blood work", "urine test", "pathology"],
        "answer": "Our Lab and Radiology center opens at 8 AM. Results are usually available in your Patient Portal within 48-72 hours."
    },
    {
        "id": 13,
        "questions": ["mental health", "therapy", "depression", "anxiety", "counseling", "psychiatrist", "psychologist", "stress"],
        "answer": "We offer Mental Health services. You can book a confidential consultation with our licensed therapists or psychiatrists."
    },
    # --- SPECIALISTS ---
    {
        "id": 14,
        "questions": ["Do you have heart doctors?", "pediatrician available?", "specialists", "doctors list", "cardiologist", "orthopedic", "surgeon", "dermatologist", "gynocologist", "ent", "eye doctor"],
        "answer": "We have specialists in Cardiology, Pediatrics, Orthopedics, and Dermatology. Visit the 'Doctors' page to see full profiles."
    },
    # --- RECORDS & VISITORS ---
    {
        "id": 15,
        "questions": ["medical records", "history", "documents", "get my file", "transfer records", "copy of records", "release form"],
        "answer": "To request medical records, fill out the release form at the front desk or download it from the 'Forms' section of our website."
    },
    {
        "id": 16,
        "questions": ["visiting hours", "visit patient", "visitor policy", "family visit", "guest", "waiting room"],
        "answer": "General visiting hours are 10 AM to 8 PM. Two visitors are allowed per patient at a time. Masks are required."
    },
    # --- GENERAL HELP ---
    {
        "id": 17,
        "questions": ["speak to human", "talk to person", "representative", "operator", "customer service", "call me", "support", "receptionist"],
        "answer": "You can reach our reception desk directly at +1-234-567-8900 (Press 0). They are available 9 AM - 6 PM."
    },
    {
        "id": 18,
        "questions": ["feedback", "complaint", "review", "compliment", "suggestion", "report issue"],
        "answer": "We value your feedback. Please email patient.relations@healthcare.plus or drop a comment card at the front desk."
    },
    {
        "id": 19,
        "questions": ["wifi", "internet", "password", "connection"],
        "answer": "Free Guest Wi-Fi is available. Network Name: 'Healthcare_Guest', Password: 'healthfirst'."
    },
    {
        "id": 20,
        "questions": ["I want to volunteer", "How can I help?", "Join the team", "jobs", "hiring", "work here", "internship", "volunteer registration", "apply"],
        "answer": "We are always looking for help! Check our 'Careers' page for jobs, or fill out the Volunteer Form in the 'Volunteer' tab."
    }
]

# --- TRAIN AI ---
all_questions = []
answers_map = []
for entry in FAQ_DATABASE:
    for q in entry['questions']:
        all_questions.append(q)
        answers_map.append(entry['answer'])

tfidf_matrix = vectorizer.fit_transform(all_questions)
print("Model Ready!")

# ==========================================
# 🛠️ HELPER FUNCTIONS
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
    message = message.lower()
    if any(w in message for w in ['pain', 'blood', 'emergency', 'chest', 'severe', 'breathing']):
        return "HIGH PRIORITY 🔴"
    elif any(w in message for w in ['fever', 'cold', 'sick', 'appointment', 'refill']):
        return "MEDIUM PRIORITY 🟡"
    return "Standard Priority 🟢"

# ==========================================
# 🌐 ROUTES
# ==========================================

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_query = data.get('query', '')
    
    # AI Search Logic
    user_vec = vectorizer.transform([user_query])
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    best_index = np.argmax(similarities)
    best_score = similarities[best_index]

    print(f"Query: {user_query} | Score: {best_score}")

    if best_score < 0.2:
        return jsonify({"success": True, "answer": "I'm not sure I understand. Could you rephrase that? Or call +1-234-567-8900."})
    
    return jsonify({"success": True, "answer": answers_map[best_index]})

@app.route('/api/patient-support', methods=['POST'])
def patient_support():
    try:
        data = request.json
        priority = analyze_urgency(data.get('message', ''))
        
        current_data = load_data(PATIENT_FILE)
        submission = {
            "id": len(current_data) + 1,
            "timestamp": datetime.now().isoformat(),
            "priority": priority,
            **data
        }
        current_data.append(submission)
        save_data(PATIENT_FILE, current_data)
        
        return jsonify({
            "success": True, 
            "message": "Request Received",
            "auto_response": f"Thank you. Marked as {priority}."
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/volunteer-registration', methods=['POST'])
def volunteer_registration():
    try:
        data = request.json
        current_data = load_data(VOLUNTEER_FILE)
        submission = {
            "id": len(current_data) + 1,
            "timestamp": datetime.now().isoformat(),
            **data
        }
        current_data.append(submission)
        save_data(VOLUNTEER_FILE, current_data)
        return jsonify({"success": True, "message": "Registered!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/admin/summary', methods=['GET'])
def get_summary():
    patients = load_data(PATIENT_FILE)
    volunteers = load_data(VOLUNTEER_FILE)
    high_priority = sum(1 for p in patients if "HIGH" in p.get('priority', ''))
    
    return jsonify({
        "total_patients": len(patients),
        "urgent_cases": high_priority,
        "total_volunteers": len(volunteers),
        "status": "Healthy"
    })

if __name__ == '__main__':
    # Ensure files exist
    if not os.path.exists(PATIENT_FILE): save_data(PATIENT_FILE, [])
    if not os.path.exists(VOLUNTEER_FILE): save_data(VOLUNTEER_FILE, [])
    
    print("🏥 Server Running...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)