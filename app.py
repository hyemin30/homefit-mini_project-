import hashlib
import jwt
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.qcokm6l.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route("/save", methods=["POST"])
def save_info():
    name_receive = request.form['name_give']
    new_id_receive = request.form['new_id_give']
    new_pw_receive = request.form['new_pw_give']
    location_receive = request.form['location_give']
    choice_receive = request.form['choice_give']
    qualification_receive = request.form['qualification_give']
    career_receive = request.form['career_give']
    img_receive = request.form['img_give']


    doc = {
        'name':name_receive,
        'new_id':new_id_receive,
        'new_pw':new_pw_receive,
        'location':location_receive,
        'choice':choice_receive,
        'qualification':qualification_receive,
        'career':career_receive,
        'img':img_receive
    }
    db.save_info.insert_one(doc)

    return jsonify({'msg':'회원가입 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)