from os import sep
import socket
import time
from tlspsk import TLSClientSession
from datetime import datetime, timedelta, timezone

def main():

    quit = False
    sock = None

    # server = '3.248.203.71'
    # port = 6000
    # server = '3.249.47.6'   34.253.244.76
    server = '34.253.244.76'
    # server = '63.34.4.88'
    port = 11111
    # server = "127.0.0.1"
    # port = 443

    def callback(data):
        nonlocal quit, sock
        print(data)
        if data == b"bye\n":
            quit = True

    psk = bytes.fromhex(
        '5a53547a59645b585b45405e5a727069'
    )
    # session = TLSClientSession(
    #     server_names="127.0.0.1", psk=psk, data_callback=callback, psk_only=True, early_data=b"hoho"
    # )
    session = TLSClientSession(
        server_names=server, psk=psk, data_callback=callback, psk_only=True
    )
    # session = TLSClientSession(server_names="127.0.0.1", data_callback=callback)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    client_hello = session.pack_client_hello()
    print('client hello: {0}'.format(client_hello.hex()))
    sock.sendall(client_hello)

    parser = session.parser()
    step = 0
    while not quit:
        step += 1
        server_data = sock.recv(10*4096)
        if len(server_data) > 0:
            print("step {0}: {1}".format(step, server_data.hex()))
        parser.send(server_data)
        data = parser.read()
        if data:
            print("data: {0}".format(data.hex()))
            sock.sendall(data)
            quit = True

    dt = datetime.utcnow()
    stime = dt.strftime('%y/%m/%d %H:%M:%S UTC')
    # data = bytes('POST /simmap/tp/ HTTP/1.1\x0d\x0aHost: localhost\x0d\x0aContent-Length: 138\x0d\x0a\x0d\x0a' +
    #              '{"iccid": "984405529081369836f5", ' +
    #              '"imei": "3a25091040261803", ' +
    #              '"tp": "test-from-python:' + stime + '"}', 'utf-8')
    # data = bytes('POST /simmap/tp/ HTTP/1.1\x0d\x0a' +
    #              'Content-Type: application/json\x0d\x0a' +
    #              'Connection: close\x0d\x0a' +
    #              'User-Agent: PodSender/0.2\x0d\x0a' +
    #              'Host: ' + server + '\x0d\x0a' +
    #              'Content-Length: 126\x0d\x0a\x0d\x0a' +
    #              '{"iccid":"984405529081369836f5",' +
    #              '"imei":"3a75250047633502",' +
    #              '"tp":"ffffffff7f9d00ffbf03021fe200000083eb0000001c4800100000000008"}', 'utf-8')

    # iot pushing telemetry data with POST
    # data_string = '{"data": "{\'temperature\': 26, \'humidity\': 41}"}'
    data_string = '{"temperature": 26, "humidity": 41}'
    # data = bytes('POST /simapp/data/51523143572089723526?iccid=984405529081369836f5 HTTP/1.1\x0d\x0a' +
    #              'Host: pod.iot.platform\x0d\x0aContent-Length: 85\x0d\x0a\x0d\x0a' +
    #              '{"iccid": "984405529081369836f5", ' +
    #              '"deviceid": "59383932333317a4", ' +
    #              '"data": "ca55a3e5"}', 'utf-8')
                 # 'Host: pod.iot.platform\x0d\x0a' +
                 # 'Content-Length: {0}\x0d\x0a\x0d\x0a{1}'.format(len(data_string), data_string), 'utf-8')
    # iot getting config data with GET
    data = bytes('GET /v1/config/51523143572089723526?iccid=984405529081369836f5 HTTP/1.1\x0d\x0a' +
                 # 'Host: pod.iot.platform\x0d\x0a\' +
                 '\x0d\x0a', 'utf-8')
    print('request: {0}'.format(data))
    app_data = session.pack_application_data(data)
    print('app_data: {0}'.format(app_data.hex()))

    sock.sendall(app_data)
    time.sleep(1)
    resp = sock.recv(4096)
    print('resp: {0}'.format(resp.hex()))
    parser.send(resp)

    time.sleep(0.5)
    resp = sock.recv(4096)
    print('resp: {0}'.format(resp.hex()))
    parser.send(resp)

    sock.sendall(session.pack_close())
    sock.close()
    print('done!')




    # quit = False
    # session = session.resumption(data_callback=callback)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((server, port))
    # sock.sendall(session.pack_client_hello())
    #
    # parser = session.parser()
    # while not quit:
    #     server_data = sock.recv(4096)
    #     parser.send(server_data)
    #     data = parser.read()
    #     if data:
    #         sock.sendall(data)
    #
    # sock.sendall(session.pack_close())
    # sock.close()


main()
