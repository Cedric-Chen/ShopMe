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


def event(my_id, friend_id):
    db = DbCtx()
    with db() as cursor:
        cursor.execute('SELECT * FROM chat WHERE user_id1=%s and user_id2=%s ORDER BY timestamp ASC',
                             (friend_id, my_id))
        result = cursor.fetchall()
        if isinstance(result, list):
            for item in result:
                cursor.execute('DELETE FROM chat WHERE user_id1=%s and user_id2=%s and timestamp=%s',
                               (friend_id, my_id, item[1]))
                yield 'data:%s \n\n' % str(item[0])
        db.commit()


@app.route('/stream/')
@app.route('/stream/<my_id>/<friend_id>/', methods=['GET', 'POST'])
def stream(my_id, friend_id):
    return Response(event(my_id, friend_id), mimetype="text/event-stream")  # response type


@app.route('/message/<my_id>/<friend_id>/<message>/')
def add_message(my_id, friend_id, message):
    db = DbCtx()
    with db() as cursor:
        args = (my_id, friend_id, message, dt.now())
        cursor.execute('INSERT INTO chat (user_id1,user_id2,text, timestamp) VALUES (%s,%s,%s, %s)', args)
        print(cursor.fetchall())
        db.commit()
    # message_box.append(message)
    # print(message_box)


if __name__ == '__main__':
    app.run()
