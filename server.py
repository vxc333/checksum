import socket
import struct

def calculate_checksum(data):
    checksum = 0
    checksums = []  # Lista para armazenar todas as cadeias de checksum
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0)
        checksum += w
        checksums.append(checksum)  # Armazena o valor parcial do checksum

    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
        checksums.append(checksum)  # Armazena o valor parcial do checksum

    return (~checksum) & 0xFFFF, checksums

def main():
    server_address = ('localhost', 12345)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)

    provoke_error = input("Deseja provocar um erro no cálculo do checksum (S/N)? ").upper()
    error_sent = False

    while True:
        data, addr = server_socket.recvfrom(1024)
        checksum = struct.unpack('>H', data[:2])[0]
        message = data[2:]

        calculated_checksum, _ = calculate_checksum(message)

        if calculated_checksum == checksum:
            if provoke_error == 'S' and not error_sent:
                print("Erro provocado - Calculando checksum incorreto")
                # Simula um erro modificando o checksum
                calculated_checksum = (calculated_checksum + 1) % 65536
                error_sent = True

            if calculated_checksum == checksum:
                print(f"Mensagem recebida: {message.decode()}")  # Imprime a mensagem recebida
                print("Checksum verificado - Enviando ACK")
                server_socket.sendto(b'Ack', addr)
            else:
                print("Checksum incorreto - NACK enviado")
                server_socket.sendto(b'Nack', addr)
        else:
            print("Mensagem corrompida - NACK enviado")
            server_socket.sendto(b'Nack', addr)

if __name__ == "__main__":
    main()
