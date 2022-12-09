from builtins import sorted

from flask import Flask, render_template, jsonify, request, make_response
from pymongo import MongoClient
from operator import itemgetter

client = MongoClient('mongodb+srv://test:sparta@cluster0.jftxkcu.mongodb.net/?retryWrites=true&w=majority')
db = client.homefit

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# 예약하기
@app.route('/tutors/reservation')
def reservation_form():
    return render_template('reservation.html')

# 예약화면으로 이동
@app.route('/tutors/reservation', methods=['POST'])
def tutors_reservation():
    num_receive = request.form['num_give']
    make_response().delete_cookie('tutorNum')
    make_response().set_cookie('tutorNum', num_receive)
    return jsonify({'msg': '예약조회'})

# 시간표 검색버튼
@app.route('/reservation', methods=["POST"])
def reservation():
    date_receive = request.form['date_give']
    # todo
    # num = request.cookies.get("tutor_num")
    num = 1
    tutor = db.tutors.find_one({'num': num})
    data = list(db.timetables.find({'tutor': tutor['id'],'date':date_receive}, {'_id': False}))
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
    member = "hyemin"

    data = db.reservations.find_one({'member': member, 'date': date_receive, 'time': time_receive})
    if data is None:
        doc = {
            'date': date_receive,
            'time': time_receive,
            'tutor': tutor,
            'member': 'hyemin'
        }
        db.reservations.insert_one(doc)
        db.timetables.delete_one({'tutor': tutor, 'time': time_receive, 'date': date_receive})
        return jsonify({'msg': '예약 완료'})
    else:
        return jsonify({'msg': '같은 시간에 다른 예약이 있습니다'})

# 예약조회화면
@app.route('/reservation/list')
def reservation_list():
    return render_template('reservation-list.html')


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

