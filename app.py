from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.xpiwifp.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/advice')
def advice():
    return render_template('advice.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')


@app.route("/tutors/search", methods=["POST"])
def tutors_post():
    type_receive = request.form['type_give']
    location_receive = request.form['location_give']

    if type_receive == '운동' and location_receive == '지역':
        tutor_list = list(db.tutors.find({}, {'_id': False}))
    else:
        tutor_list = list(db.tutors.find({'type': type_receive, 'location': location_receive}, {'_id': False}))

    return jsonify({'tutor': tutor_list})

@app.route("/review/name", methods=["POST"])
def tutor_name():
    name_receive = request.cookies.get('tutor_name')
    print(name_receive)
    print(type(name_receive))
    tutor = db.tutors.find_one({'name': name_receive})

    return jsonify({'tutor': tutor})

@app.route("/sample/add", methods=["POST"])
def sample_post():
    url_receive = request.form['url_give']
    name_receive = request.form['name_give']
    type_receive = request.form['type_give']
    location_receive = request.form['location_give']

    num = len(list(db.tutors.find({},{'_id':False}))) + 1

    doc = {
        'img': url_receive,
        'name': name_receive,
        'type': type_receive,
        'location': location_receive,
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
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': '저장 성공'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)