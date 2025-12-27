import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
load_dotenv()
app = Flask(__name__)
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-3-flash-preview")

df = pd.read_csv("qa_data (1).csv")
context_text = ""
for _,row in df.iterrows():
    context_text += f"Q: {row['question']}\nA: {row['answer']}\n"

def ask_gemini(query):
    prompt = f""" 
    You are a Q&A Assistant.
    Answers ONLY using the conext below.
    If the answer is not present, say: No relevant Q&A found.

    context: {context_text}
    Question: {query}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

#while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Good Byee!")
        

    answer = ask_gemini(user_input)
    print(answer)

@app.route("/", methods = ["GET", "POST"])
def home():
    answer = ""
    if request.method == "POST":
        query = request.form[query]
        answer = ask_gemini(query)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run()