# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import threading
import json
from swap_class import *
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)
bot = Hkuspace_bot()
main_swap_bot = Parallel_swap()


@app.route("/")
def test_page():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login_hkuspace():
    request_data = request.get_json()
    login_name = request_data["username"]
    password = request_data["password"]
    valid = bot.login_space(login_name, password)
    if valid == False:
        return {"code": 401, "message": "Unauthorized username or password"}, 401
    else:
        # bot.get_time_table()
        return {"code": 200, "message": "Successfully login"}, 200


@app.route("/login-close", methods=["GET"])
def close_login():
    valid = bot.check_login()
    if valid == True:
        return {"code": 200, "message": "Login page closed successfully"}, 200
    else:
        return {"code": 404, "message": "Google chrome not found"}, 404


@app.route("/status", methods=["GET"])
def check_status():
    valid = False
    while valid == False:
        valid = bot.check_status()
        time.sleep(5)
    return {"code": 200, "message": "The swap platform is ready"}, 200


@app.route("/check-class", methods=["POST"])
def check_class():
    request_data = request.get_json()
    class_id = request_data["course_code"]
    result = bot.swap_class_check(class_id)
    return json.dumps(result), 200


@app.route("/add-drop", methods=["POST"])
def add_drop_class():
    request_data = request.get_json()
    class_drop = request_data["origin_code"]
    class_add = request_data["new_code"]
    class_id = request_data["new_class"]
    boost = request_data["boost"]
    if boost == True:
        target = request_data["crush_num"]
        result = bot.add_drop_class(
            class_drop, class_add, class_id, boost, target)
    else:
        result = bot.add_drop_class(class_drop, class_add, class_id, boost)
    logger.debug(f"Json return: {request_data}")
    return json.dumps(result), 200


@app.route("/main-swap", methods=["POST"])
def main_swap():
    request_data = request.get_json()
    logger.debug(f"Total add-drop: {request_data}")
    username = request_data["username"]
    password = request_data["password"]
    data = request_data["data"]
    workers = len(data)
    thread1 = threading.Thread(
        target=thread_func, args=(username, password, data, workers,))
    thread1.start()
    return {"code": 200, "message": "The program started!"}


def thread_func(username, password, request_data, workers=3):
    data = [{"username": username, "password": password,
             "request_data": request_data[i]} for i in range(0, workers)]
    with ThreadPoolExecutor() as e:
        results = list(e.map(main_swap_bot.main, data))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
