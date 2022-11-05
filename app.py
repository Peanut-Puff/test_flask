import os
import time
import pymysql
from flask import Flask, url_for, render_template, abort, make_response, request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)

new_path="../static/1.jpg"
@app.route('/')
def index(image=new_path):  # put application's code here
    conn = pymysql.Connect(host='localhost', port=3306, user='root', passwd='@Hezhi11', db='exp2', charset='utf8')
    cur = conn.cursor()
    sql = "select no,name from courses1;"  # sql语句
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', time=time.ctime(), img=image, u=data)


@app.route('/gettime')
def gettime():
    return time.ctime()


@app.route('/getimg', methods=['POST', 'GET'])
def upload():
    upload_file = request.files['file']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        # 将文件保存到 static/uploads 目录，文件名同上传时使用的文件名
        new_path = os.path.join(app.root_path, 'static', filename)
        upload_file.save(new_path)
    if request.method == 'POST':
        return index("../static/" + filename)
    else:
        return new_path


@app.route('/extends/')
def extends():
    return render_template('child.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
