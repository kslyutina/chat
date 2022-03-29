import datetime
import json
from flask import Flask, render_template, request

app = Flask(__name__)

DB_FILE = "./db.json"
db = open(DB_FILE, "rb")
data = json.load(db)
messages = data["messages"]

def save_messages_to_file():
    db = open(DB_FILE, "w")
    data = {
        "messages": messages
    }
    json.dump(data, db)

def add_message(text, sender):
    now = datetime.datetime.now()
    new_message = {
        "text": text,
        "sender": sender,
        "time": now.strftime('%H:%M')
    }
    messages.append(new_message)
    save_messages_to_file()

def print_message(message):
    print(f" [{message['sender']}]: {message['text']} / {message['time']} ")

@app.route("/") #аннотация относится к след строчке
def index_page():
    return "Здравствуйте, Вас приветствует KSS CHAT"

# показать все сообщения в формате JSON
@app.route('/get_messages')
def get_messages():
    return{"messages": messages}

#показать форму чату
@app.route('./form')
def form():
    return render_template('form.html')

@app.route("/send_message")
def send_message():
    #get name and text from a user
    name = request.args["name"]
    text = request.args["text"]
    #call add_message function
    add_message (text, name)
    return "OK"

app.run(host="0.0.0.0", port=80)

