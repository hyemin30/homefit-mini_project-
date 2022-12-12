from builtins import sorted

import hashlib
import jwt
from operator import itemgetter
from datetime import datetime
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.jftxkcu.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.homefit

# client = MongoClient('mongodb+srv://test:sparta@cluster0.qcokm6l.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
# db = client.dbsparta

SECRET_KEY = 'SPARTA'


# 김현우
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
    db.members.insert_one(doc)

    return jsonify({'msg': '회원가입 완료!'})


@app.route("/api/login", methods=["POST"])
def login():
    new_id_receive = request.form['id_give']
    new_pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(new_pw_receive.encode('utf-8')).hexdigest()

    result = db.members.find_one({'new_id': new_id_receive, 'new_pw': pw_hash})

    if result is not None:
        payload = {
            'id': new_id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token, 'member_id': new_id_receive})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/save', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.members.find_one({'new_id': payload['id']}, {'_id': 0})

        return jsonify({'result': 'success', 'nickname': userinfo['name']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route('/api/id_check', methods=['GET'])
def id_check():
    print('함수호출')
    id_list = list(db.members.find({}, {'_id': False}))
    print(id_list)
    return jsonify({'id_lists': id_list})


# 유민우
@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/advise')
def advise():
    return render_template('advise.html')


@app.route('/advise/write')
def advise_write():
    return render_template('advise-write.html')


@app.route('/advise/read')
def advise_read():
    return render_template('advise-read.html')


@app.route('/review')
def review():
    return render_template('reviews.html')


@app.route("/tutors/search", methods=["POST"])
def tutors_post():
    type_receive = request.form['type_give']
    location_receive = request.form['location_give']

    if type_receive == '운동' and location_receive == '지역':
        tutor_list = list(db.members.find({'choice': "0"}, {'_id': False}))
    else:
        tutor_list = list(
            db.members.find({'choice': "0", 'type': type_receive, 'location': location_receive}, {'_id': False}))

    return jsonify({'tutor': tutor_list})


@app.route("/review/name", methods=["POST"])
def tutor_name():
    num_receive = int(request.form['num_give'])

    tutor = list(db.tutors.find({'num': num_receive}, {'_id': False}))

    return jsonify({'tutor': tutor})


@app.route("/sample/add", methods=["POST"])
def sample_post():
    url_receive = request.form['url_give']
    name_receive = request.form['name_give']
    type_receive = request.form['type_give']
    location_receive = request.form['location_give']
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    career_receive = request.form['career_give']
    qualification_receive = request.form['qualification_give']

    num = len(list(db.tutors.find({}, {'_id': False}))) + 1

    doc = {
        'img': url_receive,
        'name': name_receive,
        'type': type_receive,
        'location': location_receive,
        'id': id_receive,
        'password': password_receive,
        'career': career_receive,
        'qualification': qualification_receive,
        'num': num
    }

    db.tutors.insert_one(doc)

    return jsonify({'msg': '저장 성공'})


@app.route("/reviewSample/add", methods=["POST"])
def reviewsample_post():
    tutor_receive = request.form['tutor_give']
    member_receive = request.form['member_give']
    content_receive = request.form['content_give']

    doc = {
        'tutor': tutor_receive,
        'member': member_receive,
        'content': content_receive,
        'num': 1
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': '저장 성공'})


@app.route("/reviewTutor", methods=["POST"])
def reviewTutor():
    num_receive = int(request.form['num_give'])

    reviews = list(db.reviews.find({'num': num_receive}, {'_id': False}))

    return jsonify({'review': reviews})


@app.route("/advise/save", methods=["POST"])
def advise_save():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    private_receive = int(request.form['private_give'])
    member_id = request.cookies.get("memberId")
    member_receive = db.members.find_one({'new_id': member_id})
    temp = list(db.advise.find({}, {'_id': False}))
    num = 0

    if len(temp) == 0:
        num = 1
    else:
        for atemp in temp:
            if atemp['num'] > num:
                num = atemp['num']

    doc = {
        'title': title_receive,
        'comment': comment_receive,
        'member': member_receive,
        'id': member_id,
        'num': num + 1,
        'private': private_receive

    }

    db.advise.insert_one(doc)

    return jsonify({'msg': '상담이 완료 되었습니다!'})


@app.route("/advise/show", methods=["GET"])
def adviseShow():
    advice = list(db.advise.find({}, {'_id': False}))
    return jsonify({'advice': advice})


@app.route("/advise/show", methods=["POST"])
def myadviseShow():
    id_receive = request.cookies.get("memberId")
    advice = list(db.advise.find({'id': id_receive}, {'_id': False}))

    return jsonify({'advice': advice})


@app.route("/comment/show", methods=["POST"])
def commentShow():
    num_receive = int(request.form['num_give'])

    advice = list(db.advise.find({'num': num_receive}, {'_id': False}))

    return jsonify({'advice': advice})


@app.route("/advise/comment/find", methods=["POST"])
def commentFind():
    num_receive = int(request.form['num_give'])

    advice = list(db.advise.find({'num': num_receive}, {'_id': False}))

    return jsonify({'advice': advice})


@app.route("/advise/advice/delete", methods=["POST"])
def adviceDelete():
    num_receive = int(request.form['num_give'])

    db.advise.delete_one({'num': num_receive})

    return jsonify({'msg': '삭제 성공!'})


@app.route("/advice/modify", methods=["POST"])
def adviceModify():
    num_receive = int(request.cookies['comment_num'])
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    private_receive = int(request.form['private_give'])

    db.advise.update_one({'num': num_receive}, {'$set': {'title': title_receive}})
    db.advise.update_one({'num': num_receive}, {'$set': {'comment': comment_receive}})
    db.advise.update_one({'num': num_receive}, {'$set': {'private': private_receive}})

    return jsonify({'msg': '상담이 완료 되었습니다!'})


# 이혜민

# 예약하기
@app.route('/tutors/reservation')
def reservation_form():
    return render_template('reservation.html')


#
# # 예약화면으로 이동
@app.route('/tutors/reservation', methods=['POST'])
def tutors_reservation():
    num_receive = request.form['num_give']
    make_response().delete_cookie('tutorNum')
    res = make_response()
    res.set_cookie("tutorNum", num_receive)
    return res


# 예약화면 강사사진
@app.route('/tutors/reservation/profile', methods=['GET'])
def reservation_profile():
    tutor_num = request.cookies.get("tutorNum")
    tutor = list(db.members.find({'num': int(tutor_num),'choice':"0"}, {'_id': False}))
    return jsonify({'msg': '예약조회', 'tutor': tutor})

    make_response().set_cookie('tutorNum', num_receive)
    return jsonify({'msg': '예약조회'})


#
# 시간표 검색버튼
@app.route('/reservation', methods=["POST"])
def reservation():
    date_receive = request.form['date_give']

    num = request.cookies.get("tutorNum")
    print(num)
    print(type(num))
    tutor = db.members.find_one({'num': int(num),'choice':"0"})
    print('찾을거야',  tutor)
    data = list(db.timetables.find({'tutor': tutor['new_id'], 'date': date_receive}, {'_id': False}))
    timetables = sorted(data, key=itemgetter('time'))
    return jsonify({'timetables': timetables})


# 최종 예약버튼
@app.route('/reservation/confirm', methods=['POST'])
def reservation_confirm():
    time_receive = request.form['time_give']
    date_receive = request.form['date_give']
    tutor_num = request.cookies.get("tutorNum")
    member = request.cookies.get("memberId")
    tutor = db.members.find_one({'num': int(tutor_num),'choice':"0"})['new_id']
    member = "mini"

    data = db.reservations.find_one({'member': member, 'date': date_receive, 'time': time_receive, 'statud': 0})
    reservation_list = list(db.reservations.find({}, {'_id': False}))
    reservation_num = len(reservation_list) + 1

    if data is None:
        doc = {
            'date': date_receive,
            'time': time_receive,
            'tutor': tutor,
            'member': member,
            'num': reservation_num,
            'status': 0
        }
        db.reservations.insert_one(doc)
        db.timetables.delete_one({'tutor': tutor, 'time': time_receive, 'date': date_receive})
        res = make_response()
        res.delete_cookie('tutorNum')
        return jsonify({'msg': '예약 완료'})
    else:
        return jsonify({'msg': '같은 시간에 다른 예약이 있습니다'})


# # 예약조회화면
# @app.route('/reservation/list')
# def reservation_list():
#     return render_template('reservation-list.html')
#
# # 예약조회화면
# @app.route('/reservation/show',  methods=["GET"])
# def show_reservation():
#     # member_id = request.cookies.get("member_id")
#     member_id = 'mini'
#
#     find_tutor = db.tutors.find_one({'id': member_id})
#     find_member = db.members.find_one({'id': member_id})
#
#     if find_tutor is None:
#         print('일반회원 = ', find_member)
#         data = list(db.reservations.find({"member": find_member['id'], 'status':0}, {'_id': False}))
#         member_reservations = sorted(data, key=itemgetter('date', 'time'))
#
#         for reservation in member_reservations:
#             print(reservation)
#             date = reservation['date']
#             time = reservation['time']
#             datetime_string = date + ' ' + time
#             datetime_format = "%Y-%m-%d %H:%M"
#             datetime_result = datetime.strptime(datetime_string, datetime_format)
#             now = datetime.now()
#             print(datetime_result)
#
#             if datetime_result < now:
#                 member_reservations.remove(reservation)
#         return jsonify({'reservations':member_reservations, 'msg':'일반회원'})
#     else:
#         data = list(db.reservations.find({"tutor": find_tutor['id'], 'status':0}, {'_id': False}))
#         tutor_reservations = sorted(data, key=itemgetter('date', 'time'))
#
#         for reservation in tutor_reservations:
#             date = reservation['date']
#             time = reservation['time']
#             datetime_string = date + ' ' + time
#             datetime_format = "%Y-%m-%d %H:%M"
#             datetime_result = datetime.strptime(datetime_string, datetime_format)
#             now = datetime.now()
#             print(datetime_result)
#
#             if datetime_result < now:
#                 tutor_reservations.remove(reservation)
#
#         return jsonify({'reservations':tutor_reservations, 'msg':'강사회원'})


# 실험실 ######################################################
#
# 예약조회화면
@app.route('/reservation/list')
def reservation_list():
    return render_template('reservations.html')


@app.route('/reservation/show', methods=["POST"])
def show_reservation():
    member = request.cookies.get("memberId")
    date_receive = request.form['date_give']

    find_member = db.members.find_one({'new_id': member})

    choice = find_member['choice']
    datetime_format = "%Y-%m-%d"
    datetime_result = datetime.datetime.strptime(date_receive, datetime_format)
    now = datetime.datetime.now()
    if datetime_result < now:
        if choice == "1":
            data = list(
                db.reservations.find({"member": find_member['new_id'], 'date': date_receive, 'status': 0}, {'_id': False}))
            member_reservations = sorted(data, key=itemgetter('date', 'time'))
            print(member_reservations)
            return jsonify({'msg': '일반회원', 'status': '과거', 'reservations': member_reservations})
        else:
            data = list(
                db.reservations.find({"tutor": find_member['new_id'], 'date': date_receive, 'status': 0}, {'_id': False}))
            tutors_reservation = sorted(data, key=itemgetter('date', 'time'))
            return jsonify({'msg': '강사회원', 'status': '과거', 'reservations': tutors_reservation})
    else:
        if choice == "1":
            data = list(
                db.reservations.find({"member": find_member['new_id'], 'date': date_receive, 'status': 0}, {'_id': False}))
            member_reservations = sorted(data, key=itemgetter('date', 'time'))
            return jsonify({'msg': '일반회원', 'status': '미래', 'reservations': member_reservations})
        else:
            data = list(
                db.reservations.find({"tutor": find_member['new_id'], 'date': date_receive, 'status': 0}, {'_id': False}))
            tutors_reservation = sorted(data, key=itemgetter('date', 'time'))
            return jsonify({'msg': '강사회원', 'status': '미래', 'reservations': tutors_reservation})


#################################################################################

# 예약취소
@app.route('/reservation/cancel', methods=["POST"])
def reservation_cancel():
    num_receive = request.form['num_give']
    data = db.reservations.find_one({'num': int(num_receive)})
    tutor = data['tutor']
    date = data['date']
    time = data['time']

    doc = {
        'tutor': tutor,
        'date': date,
        'time': time
    }
    db.timetables.insert_one(doc)
    db.reservations.update_one({'num': int(num_receive)}, {'$set': {'status': 1}})

    return jsonify({'msg': '취소완료'})


# 스케줄 등록화면
@app.route('/timetables', methods=["GET"])
def show_timetables():
    member_id = request.cookies.get("memberId")
    data = db.members.find_one({'new_id': member_id, 'choice':"0"})

    if data is None:
        return jsonify({'msg': '일반회원은 이용할 수 없습니다'})
    else:
        return render_template('timetables.html')


# 스케줄 등록하기
@app.route('/timetables', methods=["POST"])
def timetables_add():
    tutor = request.cookies.get("memberId")
    time_receive = request.form['time_give']
    date_receive = request.form['date_give']

    data = db.timetables.find_one({'tutor': tutor, 'date': date_receive, 'time': time_receive})

    datetime_string = date_receive + ' ' + time_receive
    datetime_format = "%Y-%m-%d %H:%M"
    datetime_result = datetime.datetime.strptime(datetime_string, datetime_format)
    now = datetime.datetime.now()

    if datetime_result < now:
        return jsonify({'msg': '현재 시간 이후로만 등록 가능합니다'})
    else:
        if data is None:
            doc = {
                'tutor': tutor,
                'date': date_receive,
                'time': time_receive
            }
            db.timetables.insert_one(doc)
            return jsonify({'msg': '스케줄 등록 완료'})
        else:
            return jsonify({'msg': '이미 등록하였습니다'})


# 차수지

@app.route("/review", methods=["POST"])
def review_post():
    review_receive = request.form['review_give']
    review_list = list(db.review.find({},{'_id':False}))
    count = len(review_list) + 1

    member = request.cookies.get('memberId')
    tutor_num = request.cookies.get("tutorNum")
    tutor = db.members.find_one({'num': int(tutor_num), 'choice': "0"})['new_id']

    doc = {
        'member': member,
        'tutor' : tutor,
        'num':count,
        'review':review_receive,
        'done':0
    }
    db.review.insert_one(doc)

    return jsonify({'msg': '리뷰 감사합니다 😍'})


@app.route("/review/done", methods=["POST"])
def review_done():
    num_receive = request.form['num_give']
    db.review.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    return jsonify({'msg': '✏️ 등록완료'})


@app.route("/review/cancel", methods=["POST"])
def cancel_review():
    num_receive = request.form['num_give']
    db.review.delete_one({'num':int(num_receive)})
    return jsonify({'msg': '☠️ 삭제완료'})

@app.route("/review", methods=["GET"])
def review_get():
    tutor_num = request.cookies.get("tutorNum")
    tutor = list(db.members.find({'num': int(tutor_num), 'choice':"0"}, {'_id': False}))

    review_list = list(db.review.find({'tutor':tutor},{'_id':False}))
    return jsonify({'reviews': review_list})



# 여기부터는 강사프로필
@app.route("/profile", methods=["POST"])
def profile():
    current_time = datetime.datetime.now()
    image_receive = request.form['image_give']
    desc_receive = request.form['desc_give']
    file = request.files['file_give']
    ext = image_receive.split('.')[-1] #확장자 추출
    filename = f"{current_time.strftime('%Y%m%d%H%M%S')}.{ext}"
    save_to = f'static/img/tutor_profile/{filename}'  # 경로지정
    file.save(save_to)
    token_receive = request.cookies.get('mytoken')

    user = db.citista_users.find_one({'token': token_receive})
    user_id = user['username']
    content_num = db.citista_contents.find({}, {'_id': False}).collection.estimated_document_count()
    doc_contents = {
        'user_id': user_id,
        'post_id': content_num + 1,
        'img': image_receive,
        'f_name': filename,
        'desc': desc_receive,
        'timestamp': current_time
    }
    db.citista_contents.insert_one(doc_contents)
    doc_likes = {
        'post_id': content_num + 1,
        'like': 0
    }
    db.citista_likes.insert_one(doc_likes)
    return jsonify({'msg':'프로필 등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
