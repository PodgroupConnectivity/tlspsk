import socket
import time
from tls import TLSClientSession


def main():

    quit = False
    sock = None

    # server = '3.248.203.71'
    # port = 6000
    server = '3.249.47.6'
    port = 11111
    # server = "127.0.0.1"
    # port = 443

    def callback(data):
        nonlocal quit, sock
        print(data)
        if data == b"bye\n":
            quit = True

    psk = bytes.fromhex(
        '404142434445464748494a4b4c4d4e4f'
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
        server_data = sock.recv(4096)
        if len(server_data) > 0:
            print("step {0}: {1}".format(step, server_data.hex()))
        parser.send(server_data)
        data = parser.read()
        if data:
            print("data: {0}".format(data.hex()))
            sock.sendall(data)
            quit = True

    data = bytes('POST /simmap/tp/ HTTP/1.1\x0d\x0aHost: localhost\x0d\x0aContent-Length: 113\x0d\x0a\x0d\x0a' +
                 '{"iccid": "984405529081369836f5", ' +
                 '"imei": "3a25091040261803", ' +
                 '"tp": "ffffffff7f9f00dfff03021fe2000000c3fb00070411680071010000001802"}', 'utf-8')
    print('data: {0}'.format(data.hex()))
    app_data = session.pack_application_data(data)
    print('app_data: {0}'.format(app_data.hex()))

    sock.sendall(app_data)
    time.sleep(0.5)
    # resp = sock.recv(4096)
    # print('resp: {0}'.format(resp.hex()))
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
