from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(_name_)

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("prompt") or request.json.get("prompt")

    # define the message prompt FIRST
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

        # only print reply after it’s extracted
        if chat_completion and chat_completion.choices:
            reply = chat_completion.choices[0].message.content.strip()
        else:
            reply = "Hmm, I didn't get any response from the model. Try again?"

        # now safe to print debug info
        print("Prompt sent:", messages)
        print("Model replied:", reply)
        print("Full response:", chat_completion)

    except Exception as e:
        print("❌ Error talking to OpenRouter:", str(e))
        reply = "Sorry! Something went wrong while talking to the AI. Try again later."

    return jsonify({ "reply": reply })

if _name_ == "_main_":
    app.run(debug=True)
