from flask import Flask, request, jsonify, send_from_directory, session
import requests
import json
import os

app = Flask(__name__)
app.secret_key = "eduagent_secret_123"

API_KEY = os.environ.get("GROQ_API_KEY", "")
URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are EduAgent, a world-class educational assistant and expert tutor with deep knowledge across all subjects and disciplines.

Your expertise covers:
- All school and university subjects: Mathematics, Physics, Chemistry, Biology, History, Geography, Economics, Psychology, Philosophy and more
- All programming languages: Python, JavaScript, Java, C, C++, Rust, Go, TypeScript, SQL, HTML, CSS and more
- Computer Science fundamentals: Data Structures, Algorithms, Operating Systems, Networking, Databases
- AI and Machine Learning: concepts, tools, frameworks and practical applications
- Literature, Arts, Music and Humanities
- Business, Finance and Entrepreneurship

Your teaching philosophy:
- Always start with the SIMPLEST possible explanation, then gradually go deeper
- Use real world analogies that anyone can relate to
- Break every complex topic into small digestible steps
- Give practical examples and mini exercises when helpful
- Never make the student feel stupid — every question is a great question
- Check understanding by asking follow up questions
- If a student is confused, try a completely different explanation approach
- Use bullet points, numbered steps and clear structure for better readability
- For code topics, always provide clean working code examples with comments
- Celebrate progress and encourage the student constantly

Your personality:
- Patient, warm and encouraging like a favorite teacher
- Professional but friendly — not robotic
- Passionate about learning and making knowledge accessible to everyone

Your goal is to make ANY topic understandable to ANY person regardless of their background or experience level."""

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if "conversation" not in session:
        session["conversation"] = [{"role": "system", "content": SYSTEM_PROMPT}]

    user_message = request.json.get("message")
    session["conversation"].append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.1-8b-instant",
        "messages": session["conversation"]
    }

    response = requests.post(URL, headers=headers, json=body)
    data = response.json()
    reply = data["choices"][0]["message"]["content"]

    session["conversation"].append({"role": "assistant", "content": reply})
    session.modified = True

    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear():
    session.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)