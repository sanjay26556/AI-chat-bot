from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("prompt")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a smart, accurate AI assistant. Answer user questions directly, helpfully, and in detail. "
                "You are allowed to answer any question unless it's harmful. Keep it short if it's simple; go deep if it's complex."
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    try:
        chat_completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )

        if chat_completion and chat_completion.choices:
            reply = chat_completion.choices[0].message.content.strip()
        else:
            reply = "Hmm, I didn't get any response from the model. Try again?"

    except Exception as e:
        print("❌ Error talking to OpenRouter:", str(e))
        reply = "Sorry! Something went wrong while talking to the AI. Try again later."

    return jsonify({ "reply": reply })

if __name__ == "__main__":
    app.run(debug=True)
