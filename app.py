from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send
from flask_cors import CORS  # 引入 Flask-CORS
from chat import base, USER_CHAT_TEMPLATE, MODEL_CHAT_TEMPLATE

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

socketio = SocketIO(app, cors_allowed_origins="*")

model, chat_history, device = base()
model_ans = ""
stop_generation = False


@app.route('/')
def index():
    return render_template('index.html')


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


@socketio.on('message')
def handle_message(msg):
    global chat_history, model_ans, stop_generation  # 确保 chat_history, model_ans 可以被修改
    user_input = msg

    # 如果用户输入 'exit'，则不做处理
    if user_input.lower() == 'exit':
        return

    # 更新聊天历史
    chat_history += USER_CHAT_TEMPLATE.format(prompt=user_input) + "<start_of_turn>model\n"

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
    chat_history += model_ans + "<eos>\n"


if __name__ == '__main__':
    socketio.run(app, debug=True)
