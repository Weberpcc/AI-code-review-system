from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return open("index.html", encoding="utf-8").read()

@app.route("/review", methods=["POST"])
def review():
    code = request.json["code"]
    language = request.json["language"]
    focus = request.json["focus"]

    prompt = f"""You are an expert code reviewer. Review this {language} code with focus on {focus}.
If a brute force solution is detected, provide an optimized version.
Mention Big O complexity of both original and optimized solution.

Respond in EXACTLY this format with these exact headers:

CORRECTED_CODE:
[complete optimized code with perfect indentation and comments]

BUGS:
[list each bug with line number or "No bugs found"]

QUALITY:
[2-3 sentences on overall code quality]

SUGGESTIONS:
[numbered list of specific improvements]

COMPLEXITY:
Original: O(?) time, O(?) space
Optimized: O(?) time, O(?) space

SCORE: X/10
[one line reason]

Code to review:
{code}"""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        result = response.choices[0].message.content
        return jsonify({"review": result, "status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == "__main__":
    app.run(debug=True)