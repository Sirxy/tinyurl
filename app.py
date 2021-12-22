from flask import Flask, request, render_template, redirect
from cfg import Config
from util.dao import MySQL

config = {
    "HOST": Config.HOST,
    "PORT": Config.PORT,
    "USER": Config.USER,
    "PASSWORD": Config.PASSWORD,
    "DB": Config.DB,
    "CHARSET": Config.CHARSET,
}

dao = MySQL(config)

APP_HOST = Config.APP_HOST
APP_PORT = Config.APP_PORT

app = Flask(__name__)


BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(num):
    s = ""
    while num > 0:
        num, r = divmod(num, 62)
        s = BASE62[r] + s
    return s


def decode_base62(num):
    x, s = 1, 0
    for i in range(len(num) - 1, -1, -1):
        s = int(BASE62.index(num[i])) * x + s
        x *= 62
    return s


# 3、访问短URL
# 根据短，获取到长，重定向到目标URL地址
@app.route('/<string:tiny_id>')
def redirect_url_to_target(tiny_id):
    print(tiny_id, type(tiny_id))

    id = decode_base62(tiny_id)
    print(id, type(id))

    try:
        sql = """select original_url from tiny_urls where id = {pk};""".format(pk=id)
        result = dao.query_one(sql)
        return redirect(result[0])
    except Exception as e:
        raise e


# 1、首页：展示生成器的样子
@app.route('/index.html')
def index():
    return render_template('index.html')


# 2、生成短URL
@app.route('/gen_short_url', methods=["POST"])
def gen_short_url():
    original_url = request.form.get('long-url')
    print(original_url)

    try:

        sql = """insert into tiny_urls(original_url) values ("{original_url}")""".format(
            original_url=original_url,
        )
        lastrowid = dao.execute(sql)

        # 将 lastrowid 转化为 62 进制
        tiny_id = encode_base62(lastrowid)

        # 短链接
        short_url = "http://" + APP_HOST + ":" + APP_PORT + "/" + tiny_id

        return render_template('index.html', short_url=short_url)

    except Exception as e:
        raise e


if __name__ == "__main__":
    app.run(debug=True, port=5010)
