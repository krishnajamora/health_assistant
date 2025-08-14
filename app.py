from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("user_input", "")
        
        if not user_input:
            return jsonify({"response": "Please enter a message."})

        # Call Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)

        # Force clean Markdown output
        markdown_text = response.text.strip()

        return jsonify({"response": markdown_text})
    
    except Exception as e:
        return jsonify({"response": f"**Error:** {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
