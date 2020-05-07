# -*- coding: utf-8 -*-
"""
Created on Tue May  5 16:05:50 2020

@author: dm226t
"""

from flask import request
from flask import Flask, render_template
from chat import quest

app = Flask(__name__)

@app.route("/")
def home():    
    return render_template("chat.html") 

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')  
    resp=quest(userText)
    return resp.capitalize()


if __name__ == "__main__":    
    app.run(host='127.0.0.1', port=5000)
