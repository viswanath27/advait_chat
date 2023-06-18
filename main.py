from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gpt")
def gpt():
    print("Hit GPT route..")
    return render_template("gpt.html")

@app.route("/files/", methods=["POST"])
def create_file():
    print("Created the files....")
    file = request.files["file"]
    if file:
        file.save(f"uploads/{file.filename}")
        # return {"filename": file.filename}
        return render_template("index.html")
    return {"error": "No file provided."}

@app.route("/chatbot", methods=["POST"])
def chatbot_endpoint():
    user_message = request.json.get("message")
    if user_message:
        # Process the user message and generate a bot response
        # Replace the code below with your chatbot logic
        bot_message = f"Bot: You said '{user_message}'"
        return {"message": bot_message}
    return {"error": "No message provided."}


@app.route("/train-function", methods=["POST"])
def my_function():
    # Implement your function logic here
    # Access any data passed from JavaScript using request.json
    # Perform any necessary computations or actions
    # Return a response, if needed

    # For example, you can return a JSON response
    print("This is button click")

    response = {"message": "Function called successfully"}
    return jsonify(response)



if __name__ == "__main__":
    app.run(debug=True)
