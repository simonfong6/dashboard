import firebase_admin                           # Firebase interfacing
from firebase_admin import credentials, db
from keys import databaseURL, certificate       # Sensitive database info

# Reading the certificate file from Google Projects.
cred = credentials.Certificate(certificate)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': databaseURL
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
root = db.reference()
