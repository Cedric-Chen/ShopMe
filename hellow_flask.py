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

import random
import eventlet
from flask_assets import Environment

eventlet.monkey_patch()
from flask_cors import CORS, cross_origin
from flask import Flask, Response, render_template
from www.assets import bundles

app = Flask(__name__)
CORS(app)  # 注意这里的CORS
assets_env = Environment(app)
assets_env.register(bundles)


@app.route('/wechat/')
def hello_world():
    return render_template('chat.html')


def event():

    jj = 0
    if True:
        # l = len(message_box)
            yield 'data:%s \n\n' % random.random()
        # now = l
        # eventlet.sleep(1)
        # if random.random() > 0.3:
        #     message_box.append(jj)


@app.route('/stream/', methods=['GET', 'POST'])
def stream():
    return Response(event(), mimetype="text/event-stream")  # 注意这里的响应类型

def null():
    yield ""


@app.route('/message/<message>/')
def add_message(message):
    pass
    # message_box.append(message)
    # print(message_box)


if __name__ == '__main__':
    app.run()
