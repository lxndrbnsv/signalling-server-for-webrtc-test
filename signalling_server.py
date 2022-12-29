from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = "very_secret"
CORS(app)
socket_connection = SocketIO(app, cors_allowed_origins="*")


@socket_connection.on("join")
def join(message):
    username = message["username"]
    room = message["room"]
    join_room(room)

    print(f"Room Event: {username} has joined the room {room}.\n")
    emit("ready", {username: username}, to=room, skip_sid=request.sid)


@socket_connection.on("data")
def transfer_data(message):
    username = message["username"]
    room = message["room"]
    data = message["data"]
    print(f"Data Event: {username} has sent the data:\n{data}")
    emit("data", data, to=room, skip_sid=request.sid)


@socket_connection.on_error_default
def default_error_handler(e):
    print(f"Error: {e}")
    socket_connection.stop()


if __name__ == '__main__':
    socket_connection.run(app, host="0.0.0.0", port=9000)
    # socket_connection.run(app, port=9000)
