import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firebaseConfig = {
      'apiKey': "AIzaSyBqfc4B-gg7wBvqC1QBQMeq1giC1HpcYwc",
  'authDomain': "resilient-c8d95.firebaseapp.com",
  'projectId': "resilient-c8d95",
  'storageBucket': "resilient-c8d95.appspot.com",
  'messagingSenderId': "60843286594",
  'appId': "1:60843286594:web:52eeb949ced715f6cc0ddb",
  'measurementId': "G-XE7KRGQW2Z"
};
# Use the application default credentials


cred = credentials.Certificate("./creds.json")
firebase_admin.initialize_app(cred)


db = firestore.client()
doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})

doc_ref = db.collection(u'users').document(u'aturing')
doc_ref.set({
    u'first': u'raspberry',
    u'middle': u'Mathison',
    u'last': u'test',
    u'born': 1912
})