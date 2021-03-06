#-*- coding: utf-8 -*-
"""
    Micro Server For CAUP Front End
"""
import os, math, json, time, requests
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
from pymongo import MongoClient



app = Flask(__name__)
CORS(app)


Headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}
form_data = {
    'UserName': 'jllot',
    'UserPassword': 'jllot12345',
    'returnUrl': '',
    'RememberMe': 'true',
    'RememberMe': 'false'
}


@app.route('/stl-upload', methods=['POST'])
def upload_stl():
    stl_file = request.files['file']
    stl_file.save(os.path.join('./', 'temp.stl'))
    with open(os.path.join('./', 'parsed.stl'), 'w', encoding="utf-8") as out_file:
        with open(os.path.join('./', 'temp.stl'), 'r', encoding="utf-8") as in_file:
            for line in in_file:
                if 'vertex' in line:
                    numbers = line.strip().split()
                    for i in range(1, 4):
                        numbers[i] = str(round(float(numbers[i]), 2))
                    out_file.write('    ' + ' '.join(numbers) + '\n')
                elif 'facet normal' in line:
                    numbers = line.strip().split()
                    for i in range(2, 5):
                        numbers[i] = str(round(float(numbers[i]), 2))
                    out_file.write(' '.join(numbers) + '\n')
                else:
                    out_file.write(line)
    return send_from_directory('./', 'parsed.stl')


@app.route('/recievers-upload', methods=['POST'])
def upload_recievers():
    recievers = request.files['file']
    filename = secure_filename(recievers.filename)
    recievers.save(os.path.join('./', filename))
    return_string = ''
    with open(os.path.join('./', filename), 'r', encoding="utf-8") as file:
        for line in file:
            return_string += line
    return return_string


@app.route('/attachment-upload', methods=['POST'])
def upload_attachment():
    attachment = request.files['file']
    filename = secure_filename(attachment.filename)
    attachment.save(os.path.join('./', filename))
    return filename


@app.route('/send-mail', methods=['POST'])
def send_mail():
    document = {
        'usr': request.form['usr'],
        'pwd': request.form['pwd'],
        'title': request.form['title'],
        'time': request.form['time'],
        'content': request.form['content'],
        'attachment': request.form['attachment']
    }

    app.config['MAIL_USERNAME'] = document['usr']
    app.config['MAIL_PASSWORD'] = document['pwd']
    app.config['MAIL_SERVER'] = 'smtp.' + document['usr'].split('@')[1]
    app.config['MAIL_DEFAULT_SENDER'] = document['usr']
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True

    mail = Mail(app)
    msg = Message(document['title'])
    msg.body = document['content']

    if len(document['attachment']) > 0:
        with app.open_resource(document['attachment']) as fp:
            msg.attach(document['attachment'], "application/pdf", fp.read())

    recievers = []
    with open(os.path.join('./', 'reciever.txt'), 'r', encoding="utf-8") as file:
        for line in file:
            recievers.append(line.strip('\n'))

    for i in range(len(recievers)):
        msg.recipients = [recievers[i]]
        try:
            mail.send(msg)
        except:
            pass
        time.sleep(int(document['time']))
    return 'Successful!'


@app.route('/min-max', methods=['GET'])
def min_max():
    MAX = [0, -9999, -9999, -9999]
    MIN = [0, 9999, 9999, 9999]
    with open(os.path.join('./', 'parsed.stl'), 'r', encoding="utf-8") as file:
        for line in file:
            if 'vertex' in line:
                numbers = line.strip().split()
                for i in range(1, 4):
                    MAX[i] = max(MAX[i], float(numbers[i]))
                    MIN[i] = min(MIN[i], float(numbers[i]))
    json_body = {}
    json_body['x-max'] = MAX[1]
    json_body['y-max'] = MAX[2]
    json_body['z-max'] = MAX[3]
    json_body['x-min'] = MIN[1]
    json_body['y-min'] = MIN[2]
    json_body['z-min'] = MIN[3]
    return json.dumps(json_body)

@app.route('/crawl-data', methods=['GET'])
def crwal():
    json_body = {}
    s = requests.Session()

    # 获取气象站 cookie
    r = s.get('http://cloud.ssiot.com/Login/jlst', headers=Headers)
    r = s.post('http://cloud.ssiot.com/Login/jlst', data=form_data, headers=Headers)
    # 获取气象站数据
    r = s.get('http://cloud.ssiot.com/Ajax/Get/AjaxGetJsonLastDataByNodenolist.ashx?filter=GetLastDataByNodenolistalarm&nodenos=1865', headers=Headers)
    datas = json.loads(r.text)
    tmp = {}
    for data in datas['Rows']:
        if data['ShortName'] == '气压':
            continue
        tmp[data['ShortName'] + '(' + data['Unit'] + ')'] = data['Data']
    json_body['1865'] = tmp
    # 1866
    r = s.get('http://cloud.ssiot.com/Ajax/Get/AjaxGetJsonLastDataByNodenolist.ashx?filter=GetLastDataByNodenolistalarm&nodenos=1866', headers=Headers)
    datas = json.loads(r.text)
    tmp = {}
    for data in datas['Rows']:
        if data['ShortName'] == '气压':
            continue
        tmp[data['ShortName'] + '(' + data['Unit'] + ')'] = data['Data']
    json_body['1866'] = tmp

    return json.dumps(json_body)

# For web course
@app.route('/getfilm', methods=['GET'])
def get_film():
    client = MongoClient('106.14.185.200', 27017)
    DB = client['web']
    FILM = DB['film']
    j = request.args.get('iter')
    result = list(FILM.find({}, limit=200, skip=int(j)))
    return json.dumps(result, indent=2)

@app.route('/getpic', methods=['GET'])
def get_pic():
    webpage = requests.get('https://www.wf-bldgtech.com/pictest.php')
    soup = BeautifulSoup(webpage.text, 'lxml')
    element = soup.find_all('td')
    for i in range(len(element)):
        if element[i].text == '6':
            return element[i+1].text


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
