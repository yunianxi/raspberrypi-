import serial
# 初始化串行连接
ser = serial.Serial("/dev/ttyUSB0", 9600)
ser.timeout = 100  # 设置串口超时时间为1秒
print("串行通信测试开始...")
try:
    # 发送初始消息
    ser.write("Hello World!!!\n".encode())
    # 根据用户输入选择功能
    choice = input("请选择功能：1. 发送消息  2. 接收消息\n")
    choice = int(choice)  # 将用户输入的字符串转换为整数
    # 发送消息
    if choice == 1:
        while True:
            user_input = input("请输入要发送的消息（输入 q 退出）: ")
            if user_input == 'q':
                break  # 输入 q 退出循环
            ser.write((user_input + "\n").encode())  # 将用户输入转换为字节串并发送
            print("成功发送")
    # 接收消息
    elif choice == 2:
        while True:
            received_data = ser.readline().decode().strip()
            #if received_data.strip() != "":  # 去除字符串两端的空白字符，检查是否收到非空数据
            print("接收到", received_data)
    # 无效选择
    else:
        print("无效选择")

except KeyboardInterrupt:
    print("程序已终止")

finally:
    # 确保关闭串行连接
    if ser.is_open:
        ser.close()
        print("串行连接已关闭")
