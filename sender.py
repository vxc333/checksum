import socket


def calculate_checksum(data):
    checksum = sum(ord(char) for char in data)
    return ~checksum & 0xffff


def send_data(message, receiver_address, receiver_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((receiver_address, receiver_port))

    checksum = calculate_checksum(message)

    data_to_send = f"{message},{checksum}"
    sock.sendall(data_to_send.encode())

    ack = sock.recv(1024)
    print("Confirmação do destinatário:", ack.decode())
    print("Checksum: ", checksum)
    sock.close()


message = input("Digite a mensagem a ser enviada: ")
receiver_address = 'localhost'
receiver_port = 12000

send_data(message, receiver_address, receiver_port)
