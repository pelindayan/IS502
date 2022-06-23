import random
import json
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, typing
from typing import Optional, List, Dict
import pymysql

connection = pymysql.connect(host="localhost",
                                     user="root",
                                     password="chatbot123",
                                     database="metu_chatbot",
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
# domain = request.email.split('@',1)[1]
# if domain != 'metu.edu.tr':
#     message = "Not Metu email"
#     response_object = {"status": 200, "message": message}
#     return response_object

cur = connection.cursor()
query = "SELECT * FROM users WHERE email = 'pelin.dayan@metu.edu.tr'"
cur.execute(query)
query_result = cur.fetchall()
print(len(query_result))