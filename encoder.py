import serial
import struct
import time

class Encoder:
    def __init__(self, port='COM3', baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        if not self.ser.is_open:
            self.ser.open()

    def crc16(self, data: bytes) -> bytes:
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for _ in range(8):
                if crc & 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return struct.pack('<H', crc)

    def send_request(self, encoder_id: int, register: int, length: int) -> bytes:
        request = struct.pack('>B B H H', encoder_id, 0x03, register, length)
        request += self.crc16(request)
        self.ser.write(request)
        return self.ser.read(7)  # Read 7 bytes for angle data (1 byte ID, 1 byte function, 4 bytes data, 2 bytes CRC)

    def read_angle(self, encoder_id: int) -> float:
        response = self.send_request(encoder_id, 0x01, 0x01)  # 地址0x01，读取位置寄存器
        if len(response) >= 7 and self.check_crc(response):
            # 解析返回数据，前两字节为功能码和字节数
            print('response[3:5]:',response[3:5])
            angle_data = struct.unpack('>H', response[3:5])[0]  # 获取位置值
            print('angle_data:',angle_data)

            angle = angle_data / 4096 * 360  # 除以1000得到实际角度值
            print('angle:',angle)

            return angle
        return None

    def check_crc(self, response: bytes) -> bool:
        crc_received = response[-2:]
        crc_calculated = self.crc16(response[:-2])
        return crc_received == crc_calculated

    def reset_encoder(self, encoder_id: int):
        # Reset the encoder to zero point (command for register 0x0029)
        reset_command = struct.pack('>B B H H', encoder_id, 0x06, 0x0029, 0x0001)
        reset_command += self.crc16(reset_command)
        self.ser.write(reset_command)
        return self.ser.read(8)  # Response will be 8 bytes

    def close(self):
        if self.ser.is_open:
            self.ser.close()
