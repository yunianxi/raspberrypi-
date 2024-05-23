# python3
import queue
import cv2
import numpy as np
import time
import threading
import RPi.GPIO as GPIO
import random

pwm_pin1 = 17
pwm_pin2 = 27
pwm_pin3 = 23
pwm_pin4 = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin1,GPIO.OUT)
GPIO.setup(pwm_pin2,GPIO.OUT)
GPIO.setup(pwm_pin3,GPIO.OUT)
GPIO.setup(pwm_pin4,GPIO.OUT)
pwm1 = GPIO.PWM(pwm_pin1,320)
pwm2 = GPIO.PWM(pwm_pin2,320)
pwm3 = GPIO.PWM(pwm_pin3,320)
pwm4 = GPIO.PWM(pwm_pin4,320)

center = 320
target_width = 640
target_height = 480
cap = cv2.VideoCapture(0)
# 定义目标图像尺寸

roi_top = 0
roi_bottom = target_height // 2

p1 = 20
p2 = 0

# 定义一个队列作为共享变量
shared_queue = queue.Queue()
shared_queue1 = queue.Queue()
fagl = 1

def run():
	pwm1.start(p1)
	pwm2.start(p2)
	pwm3.start(p1)
	pwm4.start(p2)
#	GPIO.cleanup()

def turn_left():
	pwm1.start(p1)
	pwm2.start(p1)
	pwm3.start(p1)
	pwm4.start(p2)
#	GPIO.cleanup()

def turn_left1():
        pwm1.start(p2)
        pwm2.start(p1+10)
        pwm3.start(p1+10)
        pwm4.start(p2)
#       GPIO.cleanup()

def turn_right():
	pwm1.start(p1)
	pwm2.start(p2)
	pwm3.start(p1)
	pwm4.start(p1)
#	GPIO.cleanup()

def turn_right1():
        pwm1.start(p1+10)
        pwm2.start(p2)
        pwm3.start(p2)
        pwm4.start(p1+10)

def back():
	pwm1.start(p2)
	pwm2.start(p1)
	pwm3.start(p2)
	pwm4.start(p1)
#	GPIO.cleanup()

def stop():
	pwm1.start(0)
	pwm2.start(0)
	pwm3.start(0)
	pwm4.start(0)
#	GPIO.cleanup()

def thread1():
	"""
	线程1
	接受返回的电机速度，并进行PID计算
	"""
	# 定义上半部分区
	while (1):
		ret, frame = cap.read()
		resized_frame = cv2.resize(frame, (target_width, target_height))
		resized_frame = resized_frame[roi_top:roi_bottom, :]
		#cv2.imshow("recognize_face", resized_frame)
    		# 转化为灰度图
		gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
		#cv2.imshow("gray", gray)
		# 大津法二值化
		retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
		#cv2.imshow("dst", dst)
		# 膨胀，白区域变大
		dst = cv2.dilate(dst, None, iterations=2)
		#cv2.imshow("dst2", dst)
    		# # 腐蚀，白区域变小 #
		dst = cv2.erode(dst, None, iterations=6)
		#cv2.imshow("dst3", dst)
		# 单看第400行的像素值v
		color = dst[120]
		try:
			# 找到白色的像素点个数，如寻黑色，则改为0
			white_count = np.sum(color == 0)
        		# 找到白色的像素点索引，如寻黑色，则改为0
			white_index = np.where(color == 0)
			# 防止white_count=0的报错
			if white_count == 0:
				white_count = 1
			# 找到黑色像素的中心点位置
			# 计算方法应该是边缘检测，计算白色边缘的位置和/2，即是白色的中央位置。
			center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
        		# 计算出center与标准中心点的偏移量，因为图像大小是640，因此标准中心是320，因此320不能改。
			direction = center - 320
			#print("1~  :",direction,"---",center)
			#向队列中放入数据
			shared_queue.put(direction)
			shared_queue1.put(white_count)
			print("1~  :",direction,"---",white_count)
		except:
			continue
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


		time.sleep(0.01)




def thread2():
	"""
	线程20
	控制电机模式
	"""
	while True:
		#从队列中取出数据
		global fagl
		command = shared_queue.get()
		command1 = shared_queue1.get()
		while not shared_queue.empty():
			shared_queue.get()
		while not shared_queue1.empty():
			shared_queue1.get()
		print("2~  :", command,"---",command1)

#		turn_left()
#		back()
#		run()
#		time.sleep(1)

		if command1 > 400 and fagl == 0:
			stop()
			time.sleep(1)
		elif command1 > 400 and fagl == 1:
			turn_left1()
			time.sleep(1.4)
			fagl = 2
			stop()
			time.sleep(0.5)
		elif command1 > 400 and fagl == 2:
			turn_right1()
			time.sleep(0.8)
			fagl = 0
			stop()
			time.sleep(0.5)
		elif command > -45 and command < 45:
			run()
			time.sleep(0.001)
		elif command < -45:
			turn_right()
			time.sleep(0.001)
		elif command > 45:
			turn_left()
			time.sleep(0.001)
		else:
			stop()
			time.sleep(0.001)
		command = 0
		command1 = 0
		time.sleep(0.01)

def main():
	"""
	主线程
	"""
	GPIO.setwarnings(False)     # 关闭警告
	#GPIO.setmode(GPIO.BCM)      # BCM mode
	t1 = threading.Thread(target=thread1,name="fun_thread1",daemon=True) # 创建thread1线程
	t2 = threading.Thread(target=thread2,name="fun_thread2",daemon=True) # 创建thread2线程
	t1.start()  # 启动thread1线程
	t2.start()  # 启动thread2线程
	print("t1的线程名字是 %s" % t1.getName()) # 打印t1线程的线程名字
	print("t2的线程名字是 %s" % t2.getName()) # 打印t2线程的线程名字
	t1.join()   # 当前需要等待线程t1执行完毕后才能运行下一步
	t2.join()   # 当前需要等待线程t2执行完毕后才能运行下一步
	GPIO.cleanup() # 清除GPIO的设置
	print("主线程执行完毕！")

if __name__ == "__main__":
	main()
	GPIO.cleanup()
	cap.release()
	cv2.destroyAllWindows()
