import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate('actionserver\db\serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
# tracker_ref = db.collection(u'restaurant-bot-tracker')
# docs = tracker_ref.stream()
# print(docs)
# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')

