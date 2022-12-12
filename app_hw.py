import datetime
import hashlib
import jwt
from flask import Flask, render_template, request, jsonify, redirect, url_for



app = Flask(__name__)

# -------------------------------------------------------------------

# -------------------------------------------------------------------

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.qcokm6l.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'SPARTA'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route("/api/save", methods=["POST"])
def save_info():
    name_receive = request.form['name_give']
    new_id_receive = request.form['new_id_give']
    new_pw_receive = request.form['new_pw_give']
    location_receive = request.form['location_give']
    choice_receive = request.form['choice_give']
    qualification_receive = request.form['qualification_give']
    career_receive = request.form['career_give']
    img_receive = request.form['img_give']
    type_receive = request.form['type_give']

    pw_hash = hashlib.sha256(new_pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'name': name_receive,
        'new_id': new_id_receive,
        'new_pw': pw_hash,
        'location': location_receive,
        'choice': choice_receive,
        'qualification': qualification_receive,
        'career': career_receive,
        'img': img_receive,
        'type': type_receive
    }
    db.save_info.insert_one(doc)

    return jsonify({'msg': '회원가입 완료!'})


@app.route("/api/login", methods=["POST"])
def login():
    new_id_receive = request.form['id_give']
    new_pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(new_pw_receive.encode('utf-8')).hexdigest()

    result = db.save_info.find_one({'new_id': new_id_receive, 'new_pw': pw_hash})

    if result is not None:
        payload = {
            'id': new_id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/save', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.save_info.find_one({'new_id': payload['id']}, {'_id': 0})

        return jsonify({'result': 'success', 'name': userinfo['name']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route('/api/id_check', methods=['GET'])
def id_check():
    id_list = list(db.save_info.find({}, {'_id': False}))

    return jsonify({'id_lists': id_list})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)