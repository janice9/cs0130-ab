from flask import Flask, render_template
from flask import request
import sys
import random
import csv
import os


sys.dont_write_bytecode = True
with open('ab_test.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow([
        'version', 'pageLoadTime', 'clickTime'])
print('version', 'pageLoadTime', 'clickTime')

app = Flask(__name__)
app.config['DEBUG'] = True


# Simple python Flask server

@app.route('/', methods=['GET'])
def root():
    probability = random.uniform(0, 1)
    if probability < 0.5:
        return render_template('A.html')
    else:
        return render_template('B.html')


@app.route('/data', methods=['GET', 'POST'])
def get_data():
    json = request.get_json()
    version = json['version']
    clickTime = json['clickTime']
    pageLoadTime = json['pageLoadTime']
    print(version, pageLoadTime, clickTime)
    with open('ab_test.csv', 'a+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([version, pageLoadTime, clickTime])
    return "OK"


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
