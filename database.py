import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('serviceAccount.json')

firebase_admin.initialize_app(cred)

database = firestore.client()

id = 510864691

path = 'users'

ids = []

try:
    docs = database.collection(path).get()

    for doc in docs:
        ids.append(doc.to_dict()['id'])

    if id not in ids:
        doc_to_add = {
            'id': id
        }

        doc_ref = database.document(path + '/user_' + str(id))
        doc_ref.set(doc_to_add)
except:
    pass