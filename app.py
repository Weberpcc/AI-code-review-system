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

    prompt = f"""
You are an expert code reviewer with 10 years of experience.

Review this {language} code with focus on {focus}.
If a brute force solution is detected, provide an optimized version with better time and space complexity.
Mention the Big O complexity of both original and optimized solution.

Before reviewing think through:
1. Are there any bugs or logical errors? Which exact line?
2. Is the code efficient?
3. What is the single most important improvement?
4. Write the most optimized version of the code with perfect indentation.
   If original is O(n²), make it O(n) or O(n log n) if possible.
   Add comments explaining the optimization.

Respond in EXACTLY this format:

CORRECTED_CODE:
[complete corrected code with perfect indentation]

BUGS:
[list each bug with line number, e.g. "Line 3: variable not initialized"]
[or "No bugs found"]

QUALITY:
[2-3 sentences on overall code quality]

SUGGESTIONS:
[specific numbered suggestions for improvement with line references]

COMPLEXITY:
[Original: O(?) time, O(?) space]
[Optimized: O(?) time, O(?) space]

SCORE: X/10
[one line reason]

Code to review:
{code}
"""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return jsonify({"review": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)