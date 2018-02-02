import requests

url = 'http://localhost:8000/bookmarks/update'
payload = {'-L3S81R1z2Kec_I2EEFh': 
                {'description':'Elements of Machine Learning',
                 'resources': [
                        {'link': "http://www.svcl.ucsd.edu/courses/ece175/",
                         'title': "Class Website"},
                        {'link': "https://piazza.com/class/jcb4qckxatl65a",
                        'title': 'Piazza'}],
                  'title': "ECE 175A"}
          }

r = requests.post(url, json=payload)
print(r.json())
