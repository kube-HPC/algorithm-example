from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    # Serve the client-side application.
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)


@sio.on('my message')
def message(sid, data):
    print('message ', data)
    sio.emit('my reply', data, room='my room', skip_sid=sid)


@sio.on('initialize')
async def message(sid, data):
    print("message ", data)
    await sio.emit('initialized', data="my started data", room=sid)


@sio.on('start')
async def message(sid, data):
    print("message ", data)
    await sio.emit('started', data="my started data", room=sid)


@sio.on('stop')
async def message(sid, data):
    print("message ", data)
    await sio.emit('stopped', data="my started data", room=sid)


@sio.on('disconnect', namespace='/worker')
def disconnect(sid):
    print('disconnect ', sid)

# app.router.add_static('/static', 'static')
app.router.add_get('/', index)


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=3000)
