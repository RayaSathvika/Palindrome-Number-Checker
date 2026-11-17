"""Web application that checks whether a string is a palindrome."""

from flask import Flask, render_template, request

from palindrome import is_palindrome

app = Flask(__name__)


def evaluate(text: str) -> dict:
    cleaned = text.strip()
    if not cleaned:
        return {
            "valid": False,
            "palindrome": False,
            "message": "Enter a string to check.",
        }
    palindrome = is_palindrome(cleaned)
    status = "is a palindrome" if palindrome else "is not a palindrome"
    return {
        "valid": True,
        "palindrome": palindrome,
        "message": f'"{cleaned}" {status}.',
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    result = None
    if request.method == "POST":
        text = request.form.get("text", "")
        result = evaluate(text)
    return render_template("index.html", text=text, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070)
