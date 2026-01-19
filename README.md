# 🏥 HealthCare Plus: AI-Powered Patient Support System

![React](https://img.shields.io/badge/Frontend-React_19-blue?logo=react)
![Flask](https://img.shields.io/badge/Backend-Flask-green?logo=flask)
![AI](https://img.shields.io/badge/AI-HuggingFace_Transformers-yellow?logo=huggingface)
![Tailwind](https://img.shields.io/badge/Style-TailwindCSS-06B6D4?logo=tailwindcss)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

**HealthCare Plus** is a next-generation web application designed to modernize patient intake and support for NGOs and clinics. Unlike traditional forms, this application utilizes **Natural Language Processing (NLP)** and **Vector Embeddings** to automatically triage patients based on urgency and provide context-aware responses 24/7.

---

## ✅ Requirements & Implementation

This project fulfills all requirements of the assigned Healthcare Support Innovation Task.

| Task Requirement | Implementation in Project |
| :--- | :--- |
| **1. Create a Simple Web App** | Built a responsive Single Page Application (SPA) using **React.js** and **Tailwind CSS**. |
| **2. Basic Forms** | Implemented two distinct forms: **Patient Support** (for medical requests) and **Volunteer Registration**. |
| **3. AI / Automation Idea** | **Feature 1 (Automation):** Auto-Triage system that scans messages for urgency (High/Medium/Low) and triggers an immediate smart response.<br>**Feature 2 (Chatbot):** Semantic Search Chatbot using **Vector Embeddings** to answer FAQs without exact keywords. |
| **4. NGO Use-Case** | Designed to help understaffed NGOs filter emergency cases from routine inquiries automatically, reducing response time for critical patients. |

---

## 💡 The AI Idea & NGO Use-Case

### The Challenge
NGOs and free clinics often operate with limited staff but receive high volumes of inquiries. Critical emergencies often get buried under routine questions about hours or location, leading to delayed care.

### The Solution: "Intelligent Auto-Triage"
Instead of a simple "Thank you for submitting" message, this app uses a server-side algorithm to analyze the sentiment and keywords of every submission **in real-time**.

1.  **High Priority 🔴:** Detects words like "pain," "breathing," "blood."
    * *Action:* Flags the database entry and sends an immediate alert: *"High Priority - Nurse Notified."*
2.  **Medium Priority 🟡:** Detects "fever," "appointment," "refill."
    * *Action:* Flags entry for admin review within 24 hours.
3.  **Standard Priority 🟢:** General inquiries.
    * *Action:* Standard acknowledgment.

### Additional Feature: Semantic Chatbot
To reduce the load on human volunteers, I implemented a local AI model (Hugging Face `sentence-transformers`). Unlike basic chatbots that look for specific keywords, this bot uses **Vector Search**.
* *Example:* A user can type *"I ran out of pills"* and the AI understands this relates to **Pharmacy Hours**, even though the word "Pharmacy" was never used.



---

## 🛠️ Tech Stack & Architecture

### **Frontend (Client)**
* **React.js (v19):** Component-based UI architecture.
* **Tailwind CSS:** Responsive, modern styling.
* **Axios:** Asynchronous API communication.
* **Lucide React:** Modern iconography.

### **Backend (Server)**
* **Python Flask:** Lightweight REST API.
* **Sentence-Transformers (`all-MiniLM-L6-v2`):** State-of-the-art model for generating text embeddings locally.
* **NumPy:** Efficient vector calculations.
* **JSON Storage:** File-based persistence for easy prototyping.

---

## ⚙️ Installation & Setup Guide

Follow these steps to run the project locally.

### Prerequisites
* Node.js installed.
* Python 3.8+ installed.

### Step 1: Backend Setup
The backend handles the AI models and data storage.

1.  Navigate to the backend folder:
    ```bash
    cd backend
    ```
2.  Install the required Python libraries:
    ```bash
    pip freeze > requirements.txt
    pip install flask flask-cors sentence-transformers scikit-learn numpy
    ```
3.  Start the Server:
    ```bash
    python app.py
    ```
    > **Note:** On the very first run, it will download the AI model (approx. 80MB). Wait until you see: `✅ AI Model Loaded!`

### Step 2: Frontend Setup
The frontend handles the user interface.

1.  Open a new terminal and navigate to the frontend folder:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install axios lucide-react
    ```
3.  Start the React App:
    ```bash
    npm start
    ```
4.  Open your browser to `http://localhost:3000`.

---

## 🧪 Testing the Prototype

### Test 1: Auto-Triage (Patient Form)
1.  Go to **Patient Support**.
2.  Submit a message: *"I have severe chest pain."* -> You will see a **High Priority** alert.
3.  Submit a message: *"I need to book a checkup."* -> You will see a **Medium Priority** alert.

### Test 2: AI Chatbot
1.  Open the Chat (bottom right).
2.  Ask: *"Can I join the team?"* -> Bot understands **Volunteering**.
3.  Ask: *"My head hurts bad."* -> Bot understands **Emergency/Doctor**.

---

## 📂 Project Structure

```text
HealthCare-Plus/
│
├── .gitignore                  # Git configuration
├── README.md                   # Project Documentation
│
├── backend/
│   ├── app.py                  # Main Flask Application & AI Logic
│   ├── requirements.txt        # Backend Dependencies
│   ├── patient_submissions.json # Auto-generated Data Store
│   └── volunteer_submissions.json # Auto-generated Data Store
│
└── frontend/
    ├── public/
    │   ├── index.html          # HTML Entry Point
    │   └── favicon.ico
    ├── src/
    │   ├── App.js              # Main React Logic (Chat & Forms)
    │   ├── index.js            # React DOM Entry
    │   └── index.css           # Global Styles
    ├── package.json            # Frontend Dependencies
    └── tailwind.config.js      # Tailwind Configuration