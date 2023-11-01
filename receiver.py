import socket

def calculate_checksum(data):
    checksum = sum(ord(char) for char in data)
    return ~checksum & 0xffff

def receive_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 12000))
    sock.listen(1)

    conn, addr = sock.accept()
    print('Conexão recebida de:', addr)

    data_received = conn.recv(1024).decode()
    message, checksum_received = data_received.split(',')

    calculated_checksum = calculate_checksum(message)
    if int(checksum_received) == calculated_checksum:
        conn.sendall(b'ACK: Dados recebidos corretamente.')
        print("Mensagem recebida:", message)
        print("Checksum: ", bin(calculated_checksum)[2:])
    else:
        conn.sendall(b'NACK: Dados corrompidos. Reenviar.')

    conn.close()
    sock.close()

receive_data()
