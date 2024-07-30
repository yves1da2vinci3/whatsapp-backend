import socketio

sio_server = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])

sio_server_app = socketio.ASGIApp(socketio_server=sio_server, socketio_path="ws")


@sio_server.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio_server.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


# Chat events
@sio_server.event
async def join_chat(sid, data):
    room = data["room"]
    await sio_server.enter_room(sid, room)
    await sio_server.emit(
        "chat_message", {"msg": f"User {sid} joined chat {room}"}, room=room
    )


@sio_server.event
async def leave_chat(sid, data):
    room = data["room"]
    await sio_server.leave_room(sid, room)
    await sio_server.emit(
        "chat_message", {"msg": f"User {sid} left chat {room}"}, room=room
    )


@sio_server.event
async def send_message(sid, data):
    await sio_server.emit("send_message", data)


# Call events
@sio_server.event
async def join_call(sid, data):
    room = data["room"]
    await sio_server.enter_room(sid, room)
    await sio_server.emit(
        "call_message", {"msg": f"User {sid} joined call {room}"}, room=room
    )


@sio_server.event
async def leave_call(sid, data):
    room = data["room"]
    await sio_server.leave_room(sid, room)
    await sio_server.emit(
        "call_message", {"msg": f"User {sid} left call {room}"}, room=room
    )


@sio_server.event
async def call_message(sid, data):
    room = data["room"]
    await sio_server.emit("call_message", data, room=room)


# Story events
@sio_server.event
async def join_story(sid, data):
    room = data["room"]
    await sio_server.enter_room(sid, room)
    await sio_server.emit(
        "story_message", {"msg": f"User {sid} joined story {room}"}, room=room
    )


@sio_server.event
async def leave_story(sid, data):
    room = data["room"]
    await sio_server.leave_room(sid, room)
    await sio_server.emit(
        "story_message", {"msg": f"User {sid} left story {room}"}, room=room
    )


@sio_server.event
async def story_message(sid, data):
    room = data["room"]
    await sio_server.emit("story_message", data, room=room)
