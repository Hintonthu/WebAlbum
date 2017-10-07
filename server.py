#! /usr/bin/python3
# this python code use decode function, which must be used in python3.x
from bottle import get, post, run, request, template, route, static_file, response, redirect, debug
from config import IP_ADDRESS, PORT, end, sql_execute, sql_select
import datetime

debug(mode=True)


@route('/static/img/<filename>')
def server_static(filename):
    # this function is used to route
    # filename is the parameter of the url
    return static_file(filename, root='./static/img')


@route('/static/text/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/text')


@get("/")
def index():
    # this is the index of the web site
    count = int(request.cookies.get('count', '0'))
    count += 1
    response.set_cookie('count', str(count), max_age=3600)

    return '''
                <h1>网络相册主界面</b></h1>
                <button type="button" onclick="location.href='/upload'">上传回忆</button>
                <button type="button" onclick="location.href='/main'">我们的回忆</button>
                <h3>你已经在一个小时内看了这个网页 <b>%s</b> 次了</h3>
                <h5>@copyRight: cpak00</h5>
           ''' % (count)


@get('/main')
def main():
    # this is used to display

    divs = []

    templ = '''
    <div class="responsive">
    <div class="img">
    <a target="_blank" href="img_fjords.jpg">
    <img src=%s alt="Picture" width="300" height="200">
    </a>
    <div class="desc">%s</div>
    </div>
    </div>
    '''

    cur = sql_select('''
    SELECT * FROM UPLOAD_INFO
    ''')
    for row in cur:
        f = open(row[4])
        txt = f.readlines()
        whole = ';'.join(txt)
        divs.append(templ % (row[3], '<h5>' + str(row[0]) + '. ' + row[1] + ' '
                             + row[2] + '</h5>' + whole))

    return '''
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>weekly</title>
            <style>
            div.img {
                border: 1px solid #ccc;
            }

            div.img:hover {
                border: 1px solid #777;
            }

            div.img img {
                width: 100%;
                height: auto;
            }

            div.desc {
                padding: 15px;
                text-align: center;
            }

            * {
                box-sizing: border-box;
            }

            .responsive {
                padding: 0 6px;
                float: left;
                width: 24.99999%;
            }

            @media only screen and (max-width: 700px){
                .responsive {
                    width: 49.99999%;
                    margin: 6px 0;
                }
            }

            @media only screen and (max-width: 500px){
                .responsive {
                    width: 100%;
                }
            }

            .clearfix:after {
                content: "";
                display: table;
                clear: both;
            }
            </style>
            </head>
            <body>

            <h2 style="text-align:center">相册</h2>

            ''' + ' '.join(divs) + '''
            <div class="clearfix"></div>

            <div style="padding:6px;">
            <button type="button" onclick="location.href='/'">返回主界面</button><br/>
            <h4>@copyRight cpak00</h4>
            </div>

            </body>
            </html>
           '''


@route('/upload')
def upload():
    count = int(request.cookies.get('count', '0'))
    count += 1
    response.set_cookie('count', str(count), max_age=3600)

    return '''
        <html>
            <head>
            </head>
            <body>
                <form action"/upload" method="post" enctype="multipart/form-data">
                    
                    名字: <input type="text" name="name" /><br/>
                    图片: <input type="file" name="data" /><br/>
                    描述: <input type="text" name="describe" /><br/>
                    <input type="submit" value="上传(〃'▽'〃)" />
                    <button type="button" onclick="location.href='/'">返回主界面</button>
                </form>
            </body>
        </html>
    '''


@post("/upload", method='POST')
def form_upload():
    # this is used to upload the image and describe
    cur = sql_select("SELECT Max(ID) From UPLOAD_INFO")
    identify = 0
    for row in cur:
        if row[0] is None:
            identify = '1'
        else:
            identify = str(row[0] + 1)
    name = request.forms.get('name')
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    upload = request.files.get('data')
    path_img = "./static/img/" + identify + ".jpg"
    upload.save(path_img, overwrite=True)  # save the image

    describe = request.forms.get('describe')
    path_txt = "./static/text/" + identify + ".txt"
    f = open(path_txt, 'w+')
    print(describe)
    f.write(describe)  # save the text
    f.close()

    sql_execute('''INSERT INTO UPLOAD_INFO
    VALUES (%s,'%s','%s','%s','%s');
    ''' % (identify, name, time, path_img, path_txt))
    redirect("/")


def init():
    '''
    init
    '''
    print("init...")
    sql_execute('''CREATE TABLE IF NOT EXISTS UPLOAD_INFO 
       (ID INT PRIMARY KEY    NOT NULL,
       NAME           TEXT    NOT NULL,
       TIME           TEXT    NOT NULL,
       IMG_ADDR       TEXT,
       TEXT_ADDR      TEXT);''')

    response.set_cookie(
        'count', '0', max_age=3600)  # init the counter of this website
    # set a cookie which is used to count the number of request in an hour


try:
    init()
    run(host=IP_ADDRESS, port=PORT, reloader=True)
finally:
    end()
