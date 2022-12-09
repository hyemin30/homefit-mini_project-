from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.jftxkcu.mongodb.net/?retryWrites=true&w=majority')
db = client.homefit

#
# doc = {
#     'name': '김민지',
#     'id': 'minji',
#     'password':'1234',
#     'location': '서대문구',
#     'img' : '',
#     'career':'',
#     'qualification': '',
#     'num': 1
# }
# db.tutors.insert_one(doc)

doc2={
    'tutor': 'minji',
    'date' : '2022-12-10',
    'time': '08:00'
}

doc3={
    'tutor': 'minji',
    'date' : '2022-12-10',
    'time': '07:00'
}

doc4={
    'tutor': 'minji',
    'date' : '2022-12-10',
    'time': '17:00'
}

# db.timetables.insert_one(doc2)
# db.timetables.insert_one(doc3)

doc4={
    'name': 'hyemin',
    'id' : 'mini',
    'password': '1234'
}
# db.members.insert_one(doc4)

