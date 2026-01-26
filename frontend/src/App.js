import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot,  Phone,  Calendar, Heart, Users, MessageSquare, X, Activity } from 'lucide-react';
import axios from 'axios';

const App = () => {
  const [activeTab, setActiveTab] = useState('home');
  
  // Chatbot State
  const [chatMessages, setChatMessages] = useState([
    { type: 'bot', text: 'Hello! I am your AI health assistant. I can answer questions about hours, emergencies, or specialists. How can I help?' }
  ]);
  const [userInput, setUserInput] = useState('');
  const [chatOpen, setChatOpen] = useState(false);
  const chatEndRef = useRef(null); // Auto-scroll to bottom of chat

  // Form State
  const [formData, setFormData] = useState({
    name: '', email: '', phone: '', message: '', skills: '', availability: ''
  });
  
  // Notification State
  const [notification, setNotification] = useState({ show: false, message: '', type: '' });

  // Scroll to bottom of chat when messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  // ==========================================
  // 1. 🧠 AI CHATBOT LOGIC
  // ==========================================
  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    // Add user message immediately
    const newMessages = [...chatMessages, { type: 'user', text: userInput }];
    setChatMessages(newMessages);
    const query = userInput;
    setUserInput('');

    try {
      // Send to Flask AI Backend
      const response = await axios.post('http://localhost:5000/api/chatbot', {
        query: query
      });

      // Add AI response
      setChatMessages(prev => [...prev, { type: 'bot', text: response.data.answer }]);

    } catch (error) {
      console.error("Chat Error:", error);
      setChatMessages(prev => [...prev, { type: 'bot', text: "I'm having trouble reaching the server. Please call us directly." }]);
    }
  };

  // ==========================================
  // 2. 🚀 SMART FORM SUBMISSION (With Auto-Triage)
  // ==========================================
  const handleFormSubmit = async (formType) => {
    let url = formType === 'Patient Support' 
      ? 'http://localhost:5000/api/patient-support'
      : 'http://localhost:5000/api/volunteer-registration';

    try {
      const response = await axios.post(url, formData);

      if (response.data.success) {
        // Check if Backend sent an Auto-Response (Innovation Feature)
        const successMsg = response.data.auto_response || "Form submitted successfully!";
        
        // Show Notification
        setNotification({ show: true, message: successMsg, type: 'success' });
        
        // Hide after 6 seconds so they can read the AI analysis
        setTimeout(() => setNotification({ show: false, message: '', type: '' }), 6000);

        // Reset Form
        setFormData({ name: '', email: '', phone: '', message: '', skills: '', availability: '' });
      }
    } catch (error) {
      console.error("Form Error:", error);
      setNotification({ show: true, message: "Failed to submit. Is the backend server running?", type: 'error' });
      setTimeout(() => setNotification({ show: false, message: '', type: '' }), 4000);
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 font-sans">
      
      {/* ================= HEADER ================= */}
      <header className="bg-white shadow-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Heart className="w-6 h-6 text-white" fill="currentColor" />
            </div>
            <h1 className="text-2xl font-bold text-gray-800 tracking-tight">HealthCare Plus</h1>
          </div>
          
          <nav className="hidden md:flex gap-2">
            {['home', 'patient', 'volunteer'].map((tab) => (
              <button 
                key={tab}
                onClick={() => setActiveTab(tab)} 
                className={`px-6 py-2 rounded-full transition-all font-medium capitalize ${
                  activeTab === tab 
                    ? 'bg-blue-600 text-white shadow-md transform scale-105' 
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                {tab}
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* ================= NOTIFICATIONS ================= */}
      {notification.show && (
        <div className={`fixed top-24 right-4 max-w-md px-6 py-4 rounded-xl shadow-2xl z-50 animate-bounce ${
          notification.type === 'error' ? 'bg-red-500' : 'bg-green-600'
        } text-white`}>
          <div className="flex items-start gap-3">
            {notification.type === 'success' && <Activity className="w-6 h-6 mt-1" />}
            <div>
              <h4 className="font-bold text-lg">
                {notification.type === 'error' ? 'Error' : 'Update Received'}
              </h4>
              <p className="text-sm opacity-90">{notification.message}</p>
            </div>
          </div>
        </div>
      )}

      {/* ================= MAIN CONTENT ================= */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        
        {/* --- HOME TAB --- */}
        {activeTab === 'home' && (
          <div className="space-y-12 animate-fadeIn">
            <section className="text-center py-20 px-4">
              <h2 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6 leading-tight">
                Modern Care.<br/>
                <span className="text-blue-600">Powered by Intelligence.</span>
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10">
                Experience the future of healthcare with our AI-assisted patient support and 24/7 rapid response teams.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button onClick={() => setActiveTab('patient')} className="bg-blue-600 text-white px-8 py-4 rounded-xl text-lg font-bold hover:bg-blue-700 shadow-lg hover:shadow-blue-500/30 transition transform hover:-translate-y-1">
                  Get Immediate Support
                </button>
                <button onClick={() => setChatOpen(true)} className="bg-white text-blue-600 border-2 border-blue-100 px-8 py-4 rounded-xl text-lg font-bold hover:border-blue-600 transition">
                  Talk to AI Assistant
                </button>
              </div>
            </section>

            <section className="grid md:grid-cols-3 gap-8">
              {[
                { icon: Phone, title: "Smart Triage", desc: "Our AI analyzes your request instantly to prioritize urgent cases." },
                { icon: Users, title: "Community Driven", desc: "Join 500+ volunteers making a difference every day." },
                { icon: Calendar, title: "Instant Booking", desc: "Schedule appointments in seconds via our automated system." }
              ].map((item, idx) => (
                <div key={idx} className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-xl transition duration-300">
                  <div className="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center mb-6">
                    <item.icon className="w-8 h-8 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-bold mb-3 text-gray-900">{item.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{item.desc}</p>
                </div>
              ))}
            </section>
          </div>
        )}

        {/* --- PATIENT SUPPORT TAB --- */}
        {activeTab === 'patient' && (
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
              <div className="bg-blue-600 p-8 text-white">
                <h2 className="text-3xl font-bold mb-2">Patient Support</h2>
                <p className="opacity-90">Fill this form. Our AI will prioritize your request immediately.</p>
              </div>
              <div className="p-8 space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-2">Full Name</label>
                    <input type="text" name="name" value={formData.name} onChange={handleInputChange} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition" required />
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-2">Email</label>
                    <input type="email" name="email" value={formData.email} onChange={handleInputChange} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition" required />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">Phone Number</label>
                  <input type="tel" name="phone" value={formData.phone} onChange={handleInputChange} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition" required />
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">Describe your Symptoms / Request</label>
                  <textarea name="message" value={formData.message} onChange={handleInputChange} rows="4" className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition" placeholder="e.g., I have severe chest pain..." required></textarea>
                </div>
                <button onClick={() => handleFormSubmit('Patient Support')} className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition shadow-lg shadow-blue-500/30">
                  Analyze & Submit Request
                </button>
              </div>
            </div>
          </div>
        )}

        {/* --- VOLUNTEER TAB --- */}
        {activeTab === 'volunteer' && (
          <div className="max-w-2xl mx-auto">
             <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
              <div className="bg-green-600 p-8 text-white">
                <h2 className="text-3xl font-bold mb-2">Volunteer Registration</h2>
                <p className="opacity-90">Join our community workforce.</p>
              </div>
              <div className="p-8 space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-2">Full Name</label>
                    <input type="text" name="name" value={formData.name} onChange={handleInputChange} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 outline-none transition" required />
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-2">Email</label>
                    <input type="email" name="email" value={formData.email} onChange={handleInputChange} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 outline-none transition" required />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">Skills & Experience</label>
                  <textarea name="skills" value={formData.skills} onChange={handleInputChange} rows="3" className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 outline-none transition" required></textarea>
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">Availability</label>
                  <input type="text" name="availability" value={formData.availability} onChange={handleInputChange} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 outline-none transition" required />
                </div>
                <button onClick={() => handleFormSubmit('Volunteer')} className="w-full bg-green-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-green-700 transition shadow-lg shadow-green-500/30">
                  Submit Application
                </button>
              </div>
            </div>
          </div>
        )}

      </main>

      {/* ================= FLOATING CHATBOT ================= */}
      {!chatOpen && (
        <button
          onClick={() => setChatOpen(true)}
          className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-2xl hover:bg-blue-700 transition hover:scale-110 z-50 flex items-center gap-2 group"
        >
          <MessageSquare className="w-6 h-6" />
          <span className="max-w-0 overflow-hidden group-hover:max-w-xs transition-all duration-300 whitespace-nowrap">AI Assistant</span>
        </button>
      )}

      {chatOpen && (
        <div className="fixed bottom-6 right-6 w-96 h-[500px] bg-white rounded-2xl shadow-2xl flex flex-col z-50 animate-slideUp border border-gray-200">
          <div className="bg-blue-600 text-white p-4 rounded-t-2xl flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Bot className="w-6 h-6" />
              <div>
                <h3 className="font-bold">AI Health Assistant</h3>
                <span className="text-xs text-blue-100 flex items-center gap-1">
                  <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span> Online
                </span>
              </div>
            </div>
            <button onClick={() => setChatOpen(false)} className="hover:bg-blue-700 rounded-lg p-1 transition">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
            {chatMessages.map((msg, idx) => (
              <div key={idx} className={`flex gap-2 ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                {msg.type === 'bot' && (
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-blue-600" />
                  </div>
                )}
                <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${
                  msg.type === 'user' 
                    ? 'bg-blue-600 text-white rounded-br-none' 
                    : 'bg-white text-gray-800 shadow-sm border border-gray-100 rounded-bl-none'
                }`}>
                  {msg.text}
                </div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          <div className="p-4 bg-white border-t border-gray-100 rounded-b-2xl">
            <div className="flex gap-2">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleChatSubmit(e)}
                placeholder="Type your health question..."
                className="flex-1 px-4 py-2 bg-gray-100 border-0 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
              />
              <button onClick={handleChatSubmit} className="bg-blue-600 text-white p-2.5 rounded-xl hover:bg-blue-700 transition">
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;