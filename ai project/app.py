from flask import Flask, request, jsonify
import openai
import requests

# Set up the Flask application
app = Flask(__name__)

# Set up the OpenAI API key
openai.api_key = "your_api_key_here"

# Define a function to get the answer from ChatGPT
def get_answer(question):
    # Send the question to ChatGPT and get the response
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"What is {question}?",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    return answer

# Define a function to get the content of the URL
def get_url_content(url):
    response = requests.get(url)
    content = response.content.decode("utf-8")
    return content

# Define the Flask endpoint for answering questions
@app.route("/answer", methods=["POST"])
def answer_question():
    # Get the question from the request
    question = request.json["question"]
    # Get the content of the URL
    url = "https://university.zoominfo.com/learn/article/introduction-to-ringlead-with-guides"
    content = get_url_content(url)
    # Check if the content is related to Ringlead
    if "Ringlead" not in content:
        return jsonify({"error": "This URL is not related to Ringlead."})
    # Get the answer from ChatGPT
    answer = get_answer(question)
    # Return the answer
    return jsonify({"answer": answer})

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
