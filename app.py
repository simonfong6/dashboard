import json
from flask import Flask, redirect, url_for, session, render_template, g, request
from flask_oauth import OAuth
from functools import wraps
from keys import client_id, client_secret
 
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
    class Class:
        def __init__(self):
            self.title
            self.description
            self.resources = []
    
    classes = []
    
    ece172a =   {'title': 'ECE172A',
                 'description': 'Intro to Intelligent Systems.',
                 'resources':   [
                                 {'title': 'Class Website',
                                  'link': 'https://sites.google.com/a/eng.ucsd.edu/ece-172a-winter-2018'},
                                 {'title': 'Piazza Home',
                                  'link': 'https://piazza.com/class/jc7b0q0r4nn746?cid=8'}
                                ]
                }
    
    ece196 =   {'title': 'ECE 196',
                 'description': 'Hands on projects.',
                 'resources':   [
                                 {'title': 'Class Website',
                                  'link': 'https://ucsdece.wixsite.com/ece196'},
                                 {'title': 'Piazza',
                                  'link': 'https://piazza.com/class/jc9y5l4xia1572'}
                                ]
                }
    
    ece180 =   {'title': 'ECE 180',
                 'description': 'Software systems.',
                 'resources':   [
                                 {'title': 'Class Website',
                                  'link': 'https://share.sophorus.com/courses/ece180'},
                                 {'title': 'Piazza',
                                  'link': 'https://piazza.com/class/jcbdud70lrj7hx?cid=6'}
                                ]
                }
                
    ece175a =   {'title': 'ECE 175A',
                 'description': 'Elements of Machine Learning',
                 'resources':   [
                                 {'title': 'Class Website',
                                  'link': 'http://www.svcl.ucsd.edu/courses/ece175/'},
                                 {'title': 'Piazza',
                                  'link': 'https://piazza.com/class/jcb4qckxatl65a'}
                                ]
                }
    ece115 =   {'title': 'ECE 115',
                 'description': '',
                 'resources':   [
                                 {'title': 'TED',
                                  'link': 'https://tritoned.ucsd.edu/webapps/blackboard/content/listContent.jsp?course_id=_24780_1&content_id=_1133772_1&mode=reset'},
                                 {'title': 'Piazza',
                                  'link': 'https://piazza.com/class/jbyn4p6ve955v1'}
                                ]
                }
    
    ece107 =   {'title': 'ECE 107',
                 'description': 'Electromagnetism',
                 'resources':   [
                                 {'title': 'Class Website',
                                  'link': 'https://sites.google.com/a/eng.ucsd.edu/ece-107-winter-2018/'},
                                 {'title': '',
                                  'link': ''}
                                ]
                }
                
    ece174 =   {'title': 'ECE 174',
                 'description': 'Linear and non-linear optimization.',
                 'resources':   [
                                 {'title': 'Class Website',
                                  'link': 'http://dsp.ucsd.edu/~kreutz/ECE174.html'},
                                 {'title': 'Grade Source 4784',
                                  'link': 'http://www.gradesource.com/reports/4613/29551/index.html'}
                                ]
                }
                
    ucsd =   {'title': 'UCSD',
                 'description': 'Resources',
                 'resources':   [
                                 {'title': 'Email',
                                  'link': 'http://dsp.ucsd.edu/~kreutz/ECE174.html'},
                                 {'title': 'Outreach',
                                  'link': 'https://drive.google.com/drive/folders/0B5GEKs6sCkXNNkpqQ2JtMVFqVDQl'},
                                  {'title': 'Google Drive',
                                  'link': 'https://drive.google.com/drive/u/1/my-drive'},
                                  {'title': 'TED',
                                  'link': 'https://tritoned.ucsd.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1'},
                                  {'title': 'Web Reg',
                                  'link': 'https://act.ucsd.edu/webreg2/start'},
                                  {'title': 'Academic History',
                                  'link': 'https://act.ucsd.edu/studentAcademicHistory/academichistorystudentdisplay.htm'},
                                  {'title': 'Financial Aid',
                                  'link': 'https://act.ucsd.edu/studentFinancialAward/entry'},
                                  {'title': 'FAFSA',
                                  'link': 'https://fafsa.ed.gov/FAFSA/app/fafsa?locale=en_US'},
                                  {'title': 'Internships Tracker',
                                  'link': 'https://docs.google.com/spreadsheets/d/1miRTPlzELXdVEKzsWxgyZkFp0qFCyeiPlLFyFKyIQzY/edit#gid=0'},
                                ]
                }
    
    classes.append(ece172a)
    classes.append(ece196)
    classes.append(ece180)
    classes.append(ece175a)
    classes.append(ece115)
    classes.append(ece174)
    classes.append(ece107)
    classes.append(ucsd)
    
    return render_template('bookmarks.html', classes=classes)
 
 
def main():
    app.run(host='0.0.0.0', port=8000)
 
 
if __name__ == '__main__':
    main()
