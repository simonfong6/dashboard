import json
import firebase_admin                           # Firebase interfacing
from firebase_admin import credentials, db
from flask import Flask, redirect, url_for, session, render_template, g, request, jsonify
from flask_oauth import OAuth
from functools import wraps
from keys import client_id, client_secret, databaseURL, certificate

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = client_id
GOOGLE_CLIENT_SECRET = client_secret
REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console
 
SECRET_KEY = 'development key'
DEBUG = True
 
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()
 
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)
                          
def connect_to_db():
    """ Connect to database and return a database object. """
    # Reading the certificate file from Google Projects.
    cred = credentials.Certificate(certificate)

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': databaseURL
    })
    
connect_to_db()
 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('access_token') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')
 
 
@app.route('/google-login')
def google_login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('index'))
 
 
@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    if access_token is None:
        return redirect(url_for('login'))
 
    from urllib2 import Request, urlopen, URLError
 
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            return redirect(url_for('login'))
    
    # Check if it is the correct email
    AUTHORIZED_EMAIL = 'simonfong6@gmail.com'
    AUTHORIZED_EMAIL_1 = '1996brianhnenriquez@gmail.com'
    stuff = res.read()
    print(stuff)
    print(type(stuff))
    user = json.loads(stuff)
    if(user['email'] != AUTHORIZED_EMAIL and user['email'] != AUTHORIZED_EMAIL_1):
        return redirect(url_for('login'))
    
    session['access_token'] = access_token, ''
    
    return redirect(url_for('index'))
 
 
@google.tokengetter
def get_access_token():
    return session.get('access_token')

@app.route('/bookmarks')
@login_required    
def bookmarks():
    bookmarks = db.reference('bookmarks')
    
    bookmarks_categories = bookmarks.get()
    
    
    return render_template('bookmarks.html', 
                            bookmarks_categories=bookmarks_categories)
                            
@app.route('/bookmarks/update', methods=['GET','POST'])                              
def update_bookmarks():
    bookmarks = db.reference('bookmarks')
    
    bookmark = request.form.to_dict(flat=False)
    
    
    
    #bookmarks.update(bookmark)
    
    print(bookmark)
    if bookmark == '':
        print('empty')
    
    return jsonify({'data':'fail'})
 
 
def main():
    app.run(host='0.0.0.0', port=8000)
 
 
if __name__ == '__main__':
    main()
