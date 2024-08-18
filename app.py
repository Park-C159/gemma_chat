from flask import Flask, render_template, jsonify
from flask_cors import CORS  # 引入 Flask-CORS
from flask_socketio import SocketIO, send

from chat import base, USER_CHAT_TEMPLATE
from utils.file import *

app = Flask(__name__)

CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

socketio = SocketIO(app, cors_allowed_origins="*")

model, chat_history, device = base()
model_ans = ""
stop_generation = False
tables_created = False  # 用于追踪表是否已经创建


@app.route('/')
def index():
    return "hello world"


@app.route('/stop_chat', methods=['GET'])
def stop_chat():
    global stop_generation
    stop_generation = True
    return jsonify({"code": 200, "data": stop_generation, "msg": "成功停止"})


@app.route('/start_chat', methods=['GET'])
def start_chat():
    global stop_generation
    stop_generation = False
    return jsonify({"code": 200, "data": stop_generation, "msg": "成功开启"})


chat_file = "./files/chat_1.txt"


@app.route('/restart_chat', methods=['Delete'])
def restart_chat():
    global history_chat
    isDeleted = delete_file(chat_file)
    if isDeleted:
        append_to_file(chat_file, USER_CHAT_TEMPLATE.format(prompt="请用中文回答后面所有的问题。"))
        return jsonify({"code": 200, "msg": "删除成功！"})
    else:
        return jsonify({"code": 404, "msg": "删除失败！"})


@app.route('/history_chat', methods=['GET'])
def history_chat():
    global chat_history
    if check_file_exists(chat_file):
        chat_history = read_file(chat_file)
        data = parse_conversation(chat_history)

        return jsonify({"code": 200, "data": data, "msg": "加载成功！"})
    else:
        append_to_file(chat_file, USER_CHAT_TEMPLATE.format(prompt="请用中文回答后面所有的问题。"))
        return jsonify({"code": 200, "data": chat_history, "msg": "初始化成功！"})


@socketio.on('message')
def handle_message(msg):
    global chat_history, model_ans, stop_generation  # 确保 chat_history, model_ans 可以被修改
    user_input = msg

    # 如果用户输入 'exit'，则不做处理
    if user_input.lower() == 'exit':
        return

    # 更新聊天历史
    chat_history += USER_CHAT_TEMPLATE.format(prompt=user_input) + "<start_of_turn>model\n"

    res = ""

    # 模型生成回答并实时发送给客户端
    for model_ans in model.generate_and_stream(
            prompts=chat_history,
            device=device,
            output_len=512
    ):
        if stop_generation:
            stop_generation = False
            break
        send(model_ans, broadcast=True)
        res += model_ans

    append_to_file(chat_file,
                   USER_CHAT_TEMPLATE.format(prompt=user_input) + "<start_of_turn>model\n" + res + "<eos>\n")
    chat_history += res + "<eos>\n"


if __name__ == '__main__':
    socketio.run(app, debug=True)
