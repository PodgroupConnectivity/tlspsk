import socket
from tls import TLSClientSession


def main():

    quit = False
    sock = None

    server = "127.0.0.1"
    port = 443

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
    sock.sendall(session.pack_client_hello())

    parser = session.parser()
    step = 0
    while not quit:
        step += 1
        server_data = sock.recv(4096)
        print("step {0}: {1}".format(step, server_data.hex()))
        parser.send(server_data)
        data = parser.read()
        if data:
            print("data: {0}".format(data.hex()))
            sock.sendall(data)

    sock.sendall(session.pack_close())
    sock.close()




    quit = False
    session = session.resumption(data_callback=callback)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    sock.sendall(session.pack_client_hello())

    parser = session.parser()
    while not quit:
        server_data = sock.recv(4096)
        parser.send(server_data)
        data = parser.read()
        if data:
            sock.sendall(data)

    sock.sendall(session.pack_close())
    sock.close()


main()
