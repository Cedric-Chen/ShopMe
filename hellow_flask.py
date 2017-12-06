# from flask import Flask
#
# app = Flask(__name__)
#
#

#
#
# if __name__ == '__main__':
#     app.run()

# coding=utf-8
'''
@Author：Roy.S
@CreateDate： 2016年 08月 04日 星期四 10:56:37 HKT
@Description：配合html5测试服务端推送事件
'''

from config import app
import random
from datetime import datetime as dt
import eventlet
from flask_assets import Environment

eventlet.monkey_patch()
from database.mysql.engine import DbCtx
from flask_cors import CORS, cross_origin
from flask import Flask, Response, render_template
from www.assets import bundles

CORS(app)  # 注意这里的CORS
assets_env = Environment(app)
assets_env.register(bundles)


@app.route('/wechat/')
def hello_worlds():
    return render_template('chat.html')


def event():
    timestamp = dt.now()
    db = DbCtx()
    with db() as cursor:
        ret = cursor.execute('SELECT * FROM wechat ORDER BY timestamp ASC')
        result = cursor.fetchall()
        if isinstance(result,list):
            for item in result:
                cursor.execute('DELETE FROM wechat WHERE timestamp=%s', (item[1],))
                yield 'data:%s \n\n' % str(item[0])
        db.commit()


@app.route('/stream/', methods=['GET', 'POST'])
def stream():
    return Response(event(), mimetype="text/event-stream")  # response type


@app.route('/message/<message>/')
def add_message(message):
    db = DbCtx()
    with db() as cursor:
        args = (message, dt.now())
        cursor.execute('INSERT INTO wechat (text, timestamp) VALUES (%s, %s)', args)
        print(cursor.fetchall())
        db.commit()
    # message_box.append(message)
    # print(message_box)


if __name__ == '__main__':
    app.run()
