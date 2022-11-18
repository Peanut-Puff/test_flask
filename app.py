import os
import time
import random
from flask import Flask, url_for, render_template, abort, make_response, request
from werkzeug.utils import secure_filename

from utils import db_util

ALLOWED_EXTENSIONS = {'png', 'jpg', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)

new_path = "../static/img/1.jpg"


@app.route('/upload')
def upload(image=new_path):  # put application's code here
    mydb = db_util('localhost', 3306, 'root', '@Hezhi11', 'exp2', )
    mydb.connect()
    mydb.select_all('select * from file')
    mydb.close()
    return render_template('upload.html', time=time.ctime(), img=image, u=mydb.data)


@app.route('/gettime')
def gettime():
    return time.ctime()


@app.route('/upload', methods=['POST', 'GET'])
def getfile():
    if request.method == 'POST':
        upload_file = request.files['file']
        if upload_file and allowed_file(upload_file.filename):
            filename = secure_filename(upload_file.filename)
            if '.'not in filename:
                filename=str(random.randint(1000,9999))+"."+filename
            # 将文件保存到 static/uploads 目录，文件名同上传时使用的文件名
            new_path = os.path.join(app.root_path, 'static\\img', filename)
            upload_file.save(new_path)
            path="../static/img/" + filename
            mydb = db_util('localhost', 3306, 'root', '@Hezhi11', 'exp2', )
            mydb.connect()
            statu=mydb.execute("insert into file(name,path)values('%s','%s')" % (filename,path))
            mydb.close()
            if statu==0:
                return upload(path)
            else:
                return upload()


@app.route('/gallery')
def gallery(path="../static/img/1.jpg",name="Example Image"):  # put application's code here
    mydb = db_util('localhost', 3306, 'root', '@Hezhi11', 'exp2', )
    mydb.connect()
    mydb.select_all('select name from file')
    mydb.close()
    return render_template('gallery.html',n=mydb.data.__len__(),u=mydb.data,imgpath=path,imgname=name)


@app.route('/gallery', methods=['POST', 'GET'])
def getpath():
    if request.method == 'POST':
        option = request.form.get("selectpic")
        mydb = db_util('localhost', 3306, 'root', '@Hezhi11', 'exp2', )
        mydb.connect()
        mydb.select_all('select * from file')
        mydb.close()
        path=mydb.data[int(option)-1][1]
        name=mydb.data[int(option)-1][0]
        return gallery(path,name)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
