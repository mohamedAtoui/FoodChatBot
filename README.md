# FoodChatBot
A food chatbot is an AI-driven application designed to assist users in ordering food and retrieving related information


## Features

- Place new orders
- Track existing orders
- Remove items from orders
- Complete orders

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/food-chatbot.git
   cd food-chatbot

## Install dependencies
pip install -r requirements.txt

## Run the application:
uvicorn main:app --reload

## app/routers/order.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

router = APIRouter()

@router.post("/")
async def handle_request(request: Request):
    # Same implementation as in main.py
    pass
## app/db/db_connection.py

import mysql.connector

def get_db_connection():
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='pandeyji_eatery'
    )
    return cnx

