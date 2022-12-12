from builtins import sorted

from flask import Flask, render_template, jsonify, request, make_response
from pymongo import MongoClient
import certifi
from operator import itemgetter
from datetime import datetime
ca = certifi.where()
# client = MongoClient('mongodb+srv://test:sparta@cluster0.jftxkcu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
# db = client.homefit

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.xpiwifp.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

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
    return render_template('review.html')

@app.route("/tutors/search", methods=["POST"])
def tutors_post():
    type_receive = request.form['type_give']
    location_receive = request.form['location_give']

    if type_receive == '운동' and location_receive == '':
        tutor_list = list(db.members.find({}, {'_id': False}))
    else:
        tutor_list = list(db.members.find({'type': type_receive, 'location': location_receive}, {'_id': False}))

    return jsonify({'tutor': tutor_list})

@app.route("/review/name", methods=["POST"])
def tutor_name():
    num_receive = int(request.form['num_give'])

    tutor = list(db.members.find({'num':num_receive},{'_id':False}))

    return jsonify({'tutor': tutor})

@app.route("/reviewTutor", methods=["POST"])
def reviewTutor():
    num_receive = int(request.form['num_give'])

    reviews = list(db.reviews.find({'num':num_receive},{'_id':False}))

    return jsonify({'review': reviews})

@app.route("/advise/save", methods=["POST"])
def advise_save():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    private_receive = int(request.form['private_give'])
    member_receive = '테스트2'
    member_id = 'test1234'
    #member 이름과 아이디는 현재 접속중인 사람의 것을 넣음
    temp = list(db.advise.find({}, {'_id': False}))
    num = 0

    if len(temp) == 0 :
        num = 1
    else :
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
    advice = list(db.advise.find({},{'_id':False}))

    return jsonify({'advice': advice})

@app.route("/advise/show", methods=["POST"])
def myadviseShow():
    id_receive = request.form['id_give']

    advice = list(db.advise.find({'id': id_receive}, {'_id': False}))

    return jsonify({'advice': advice})

@app.route("/comment/show", methods=["POST"])
def commentShow():
    num_receive = int(request.form['num_give'])

    advice = list(db.advise.find({'num':num_receive},{'_id':False}))

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

    db.advise.update_one({'num':num_receive},{'$set':{'title': title_receive}})
    db.advise.update_one({'num': num_receive}, {'$set': {'comment': comment_receive}})
    db.advise.update_one({'num': num_receive}, {'$set': {'private': private_receive}})

    return jsonify({'msg': '상담이 완료 되었습니다!'})

@app.route('/')
def home():
    return render_template('index.html')

#예약하기
@app.route('/tutors/reservation')
def reservation_form():
    return render_template('reservation.html')
#
# # 예약화면으로 이동
@app.route('/tutors/reservation', methods=['POST'])
def tutors_reservation():
    num_receive = request.form['num_give']
    make_response().delete_cookie('tutorNum')
    make_response().set_cookie('tutorNum', num_receive)
    return jsonify({'msg': '예약조회'})
#
# 시간표 검색버튼
@app.route('/reservation', methods=["POST"])
def reservation():
    date_receive = request.form['date_give']

    # todo
    # num = request.cookies.get("tutor_num")
    num = 1
    tutor = db.tutors.find_one({'num': num})
    data = list(db.timetables.find({'tutor': tutor['id'], 'date': date_receive}, {'_id': False}))
    timetables = sorted(data, key=itemgetter('time'))
    return jsonify({'timetables': timetables})

# 최종 예약버튼
@app.route('/reservation/confirm', methods=['POST'])
def reservation_confirm():
    time_receive = request.form['time_give']
    date_receive = request.form['date_give']
    # todo
    # tutor_num = request.cookies.get("tutor_num")
    # member_id = request.cookies.get("member_id")
    num = 1
    tutor = db.tutors.find_one({'num': num})['id']
    member = "mini"


    data = db.reservations.find_one({'member': member, 'date': date_receive, 'time': time_receive, 'statud':0})
    reservation_list = list(db.reservations.find({}, {'_id': False}))
    reservation_num = len(reservation_list) +1

    if data is None:
        doc = {
            'date': date_receive,
            'time': time_receive,
            'tutor': tutor,
            'member': member,
            'num': reservation_num,
            'status':0
        }
        db.reservations.insert_one(doc)
        db.timetables.delete_one({'tutor': tutor, 'time': time_receive, 'date': date_receive})
        return jsonify({'msg': '예약 완료'})
    else:
        return jsonify({'msg': '같은 시간에 다른 예약이 있습니다'})
#
# 예약조회화면
@app.route('/reservation/list')
def reservation_list():
    return render_template('reservation-list.html')

# 예약조회화면
@app.route('/reservation/show',  methods=["GET"])
def show_reservation():
    # member_id = request.cookies.get("member_id")
    member_id = 'mini'

    find_tutor = db.tutors.find_one({'id': member_id})
    find_member = db.members.find_one({'id': member_id})

    if find_tutor is None:
        print('일반회원 = ', find_member)
        data = list(db.reservations.find({"member": find_member['id'], 'status':0}, {'_id': False}))
        member_reservations = sorted(data, key=itemgetter('date', 'time'))

        for reservation in member_reservations:
            print(reservation)
            date = reservation['date']
            time = reservation['time']
            datetime_string = date + ' ' + time
            datetime_format = "%Y-%m-%d %H:%M"
            datetime_result = datetime.strptime(datetime_string, datetime_format)
            now = datetime.now()
            print(datetime_result)

            if datetime_result < now:
                member_reservations.remove(reservation)
        return jsonify({'reservations':member_reservations, 'msg':'일반회원'})
    else:
        data = list(db.reservations.find({"tutor": find_tutor['id'], 'status':0}, {'_id': False}))
        tutor_reservations = sorted(data, key=itemgetter('date', 'time'))

        for reservation in tutor_reservations:
            date = reservation['date']
            time = reservation['time']
            datetime_string = date + ' ' + time
            datetime_format = "%Y-%m-%d %H:%M"
            datetime_result = datetime.strptime(datetime_string, datetime_format)
            now = datetime.now()
            print(datetime_result)

            if datetime_result < now:
                tutor_reservations.remove(reservation)

        return jsonify({'reservations':tutor_reservations, 'msg':'강사회원'})

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

    # member_id = request.cookies.get("member_id")
    member_id = 'minji'

    data = db.tutors.find_one({'id': member_id})

    if data is None:
        return jsonify({'msg': '일반회원은 이용할 수 없습니다'})
    else:
        return render_template('timetables.html')


# 스케줄 등록하기
@app.route('/timetables', methods=["POST"])
def timetables_add():
    # tutor = request.cookies.get("member_id")
    tutor = 'minji'
    time_receive = request.form['time_give']
    date_receive = request.form['date_give']

    data = db.timetables.find_one({'tutor': tutor, 'date': date_receive, 'time':time_receive})

    datetime_string = date_receive + ' ' + time_receive
    datetime_format = "%Y-%m-%d %H:%M"
    datetime_result = datetime.strptime(datetime_string, datetime_format)
    now = datetime.now()

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)