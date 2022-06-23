import random
import json
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, typing
from typing import Optional, List, Dict
import pymysql

import nltk
from nltk.stem import WordNetLemmatizer
from random import randint


from tensorflow.keras.models import load_model
app = FastAPI(title="Chat Bot")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lemmatizer= WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')


def random_with_N_digits():
    range_start = 10**(5)
    range_end = (10**6)-1
    return randint(range_start, range_end)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_TRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_TRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    print(intents_list)
    tag = intents_list[0]['intent']
    probability = intents_list[0]['probability']
    if float(probability) < 0.80:
        return "Sorry, I am not sure what you need. Can I help you with anything else?"
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['answer'])
            break
    return result

print("Go! Bot is running!")

class SignupRequest(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    address: Optional[str]
    email: Optional[str]
    password: Optional[str]

class SignupResult(SignupRequest):
    status: Optional[int]
    message: Optional[str]

class LoginRequest(BaseModel):
    email: Optional[str]
    password: Optional[str]

class LoginResult(LoginRequest):
    status: Optional[int]
    message: Optional[str]

class PredictRequest(BaseModel):
    text: Optional[str]
    user: Optional[str]

class PredictResult(LoginRequest):
    response: Optional[str]
    status: Optional[int]
    message: Optional[str]

def insertQuestion(user, question, answer):
    connection = pymysql.connect(host="localhost",
                                     user="root",
                                     password="chatbot123",
                                     database="metu_chatbot",
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    randomNumber = random_with_N_digits()
    insertQuery = "INSERT INTO `questions` (`user_email`, `question_text`, `response_text`,`response_id`) VALUES (%s, %s, %s, %s)" 
    cur.execute(insertQuery, (user, question, answer, str(randomNumber)))
    connection.commit()

@app.post("/predict",response_model=PredictResult)
async def get_result_from_chatbot(request: PredictRequest, response: Response):
    question = request.text
    user = request.user
    ints = predict_class(question)
    if ints:
        res = get_response(ints, intents)
        insertQuestion(user, question, res)
        response_object = {"response": res, "status": 200, "message": "Success"}
        return response_object
    else:
        insertQuestion(user, question, "Sorry, I am not sure what you need. Can I help you with anything else?")
        response_object = {"response": "No comment", "status": 200, "message": "Success"}
        return response_object

@app.post("/login", response_model=LoginResult)
async def login_function(request: LoginRequest, response: Response):
    connection = pymysql.connect(host="localhost",
                                     user="root",
                                     password="chatbot123",
                                     database="metu_chatbot",
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    query = "SELECT * FROM users WHERE email = '" + request.email + "'"
    cur.execute(query)
    query_result = cur.fetchall()
    if len(query_result) == 0:
         message = "Email is not registered"
         response_object = {"status": 200, "message": message}
         return response_object
    for line in query_result:
        if request.password == line["password"]:
            message = "Its Valid"
        else:
            message = "Password is not correct"
        response_object = {"status": 200, "message": message}
    return response_object

@app.post("/signup", response_model=SignupResult)
async def signup_function(request: SignupRequest, response: Response):
    connection = pymysql.connect(host="localhost",
                                     user="root",
                                     password="chatbot123",
                                     database="metu_chatbot",
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

    domain = request.email.split('@',1)[1]
    if domain != 'metu.edu.tr':
        message = "Please enter your METU email"
        response_object = {"status": 200, "message": message}
        return response_object

    cur = connection.cursor()
    query = "SELECT * FROM users WHERE email = '" + request.email + "'"
    cur.execute(query)
    query_result = cur.fetchall()
    if len(query_result) != 0:
        message = "Already Signed Up"
        response_object = {"status": 200, "message": message}
        return response_object
    insertString = "('" + request.name + "', '" + request.surname+ "', '" + request.address+ "', '" + request.email+ "', '" + request.password +"')"
    insertQuery = "INSERT INTO `users` (`name`, `last_name`, `address`, `email`, `password`) VALUES " + insertString    
    cur.execute(insertQuery)
    connection.commit()
    message = "Signup Completed"
    response_object = {"status": 200, "message": message}
    return response_object