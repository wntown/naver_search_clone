from flask import Flask, render_template, jsonify
import naverpop
import time
import threading
import datetime
 
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rank")
def get_rank():
    f = open("new_list.json","r",encoding='utf8')
    data = f.read()
    f.close()
    return jsonify(data)


def auto_thread(): # 60초마다 naverpop.py 에있는 파일을 가져와서 json파일(new_list.json) 을 갱신
    naverpop.auto_run()
    threading.Timer(60, auto_thread).start()



if __name__ == "__main__":
    auto_thread()
    app.run(debug=True, threaded=True)