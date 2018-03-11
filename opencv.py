# -*- coding=UTF-8 -*-

import cv2
import smtplib
from email.mime.text import MIMEText

OPENCV_PATH='C:\\Users\\bob\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\cv2\\data'
classfier = cv2.CascadeClassifier(OPENCV_PATH+'\haarcascade_frontalface_alt2.xml')

def sendmail(msg_from, passwd, msg_to, subject, content):
	msg_from='xx' if not msg_from else msg_from 
	passwd='xx' if not passwd else passwd
	msg_to='xx' if not msg_to else msg_to

	subject='python邮件测试'
	content='这是我用python smtplib及email模块发送的邮件'
	msg=MIMEText(content)
	msg['Subject'] = subject
	msg['From'] = msg_from
	msg['To'] = msg_to

	try:
		s = smtplib.SMTP_SSL("smtp.qq.com", 465)
		s.login(msg_from, passwd)
		s.sendmail(msg_from, msg_to, msg.as_string())
		print("发送成功")
	except s.SMTPException as e:
		print("发送失败")
	finally:
		s.quit()

def humanface_detect(classfier):
	cap = cv2.VideoCapture(0)
	color = (0,255,0)
	while(1):
		ret,frame = cap.read()
		while not ret:
			break
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faceRects = classfier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32,32))
		if len(faceRects) > 0:
			for faceRect in faceRects:
				x,y,w,h = faceRect
				cv2.rectangle(frame, (x-10,y-10), (x+w+10, y+h+10), color, 2)
		cv2.imshow('human face detection',frame)
		key = cv2.waitKey(1)
		if ((key & 0xFF) == ord('q')):
			sendmail()
			break
	cap.release()
	cv2.destroyAllWindows()

if __name__=='__main__':
	
	humanface_detect(classfier)
