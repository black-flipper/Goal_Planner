from flask import Flask, render_template_string, request
import cohere

app = Flask(__name__)

# Replace 'your-cohere-api-key' with your actual Cohere API key
COHERE_API_KEY = "eMHvYcpnwcRWImPPESsOipnEsOAAdIncBidKKk7F"
co = cohere.Client(COHERE_API_KEY)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Goal Achiever</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }
        .container {
            max-width: 600px;
            margin: auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        textarea, button {
            margin-top: 10px;
            padding: 10px;
            font-size: 16px;
        }
        textarea {
            height: 100px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            background-color: #f1f1f1;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Goal Achiever</h1>
        <form method="post">
            <label for="goal">What is your goal?</label>
            <textarea name="goal" id="goal" placeholder="Enter your goal..."></textarea>
            <button type="submit">Get Steps</button>
        </form>

        {% if steps %}
        <div class="result">
            <h2>Steps to Achieve Your Goal:</h2>
            <p><strong>Goal:</strong> {{ goal }}</p>
            <p>{{ steps }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_goal = request.form.get("goal")
        response = co.generate(
            model="command-xlarge-nightly",
            prompt=f"My goal is: {user_goal}\nCan you give me detailed steps to achieve this goal?",
            max_tokens=300,
            temperature=0.7,
            stop_sequences=["\n"]
        )
        steps = response.generations[0].text.strip()
        return render_template_string(HTML_TEMPLATE, steps=steps, goal=user_goal)

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)
