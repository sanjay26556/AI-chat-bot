from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)
pipe = pipeline("text-generation", model="deepseek-ai/deepseek-coder-1.3b-instruct")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("user_input") or request.json.get("user_input")
    prompt = f"Please explain this in simple terms: {user_input}"
    result = pipe(prompt, max_new_tokens=150, do_sample=True)[0]["generated_text"]
    reply = result.replace(prompt, "").strip()
    return jsonify({ "reply": reply })

if __name__ == "__main__":
    app.run(debug=True)