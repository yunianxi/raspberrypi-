import RPi.GPIO as GPIO  #导入gpio口驱动模块
import time              #导入时间模块
pwm_pin = 23             #定义pwm输出引脚

GPIO.setmode(GPIO.BCM)   #定义树莓派gpio引脚以BCM方式编号
GPIO.setup(pwm_pin,GPIO.OUT)  #使能gpio口为输出
pwm = GPIO.PWM(pwm_pin,320)   #定义pwm输出频率
while 1:
	for i in range(0,70):       #for循环调整脉宽
		print("ok")               #输出提示
		pwm.start(i)              #启动pwm
		time.sleep(0.01)
	time.sleep(1)           #延时

	for j in range(70,0,-1):
		print("yes")
		pwm.start(j)
		time.sleep(0.01)
	time.sleep(1)

pwm.stop()                   #关闭pwm输出
GPIO.cleanup()               #释放gpio口

