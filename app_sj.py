import datetime

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.n0imoeb.mongodb.net/cluster0?retryWrites=true&w=majority', tlsCAFile=ca )
db = client.test


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/review", methods=["POST"])
def review_post():
    review_receive = request.form['review_give']
    review_list = list(db.review.find({},{'_id':False}))
    count = len(review_list) + 1

    doc = {
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
    review_list = list(db.review.find({},{'_id':False}))


    return jsonify({'reviews': review_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)





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