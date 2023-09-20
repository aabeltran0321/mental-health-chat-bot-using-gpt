from flask import Flask, request, render_template
# import openai
from openai_module import ChatApp


app = Flask(__name__)

# Your chatbot logic goes here
@app.route("/")
def index():
    global ChatApp1
    ChatApp1 = ChatApp(
    token="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",
    system_role="You are a health expert, health advisor, and health professional. Answer this question. Make it short but informative. Rate Distress Level and Anxiety Level in Low, Moderate, or High if necessary. Prettify your response.")
    return render_template("mentalhealth.html")

@app.route("/send-message", methods=["POST"])
def send_message():
    global ChatApp1
    user_input = request.get_json()["user_input"]
    # bot_response = chat_response(user_input)
    #bot_response = HealthAdvisor(user_input)
    bot_response = ChatApp1.chat(user_input)
    return {"response": bot_response}




if __name__ == "__main__":
    app.run(debug=True, port="8000",host="0.0.0.0")
