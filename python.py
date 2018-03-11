# _*_ coding=UTF-8 _*_
# 1.type and object
# 所有的类型都是object的子类，除了object
# 所有的类型都是type的实例，包括type
print(object)			#int本身是一种class
print(type(object))		#object是type的实例
print(object.__class__) #object是type的实例
print(object.__bases__) #object没有父类
print(int)  			#int本身是一种class
print(type(int))		#int是type的实例
print(int.__class__)	#int是type的实例
print(int.__bases__)	#int的父类是object类
print(type)				#type本身是一种class
print(type(type))		#type是type的实例
print(type.__class__)	#type是type的实例
print(type.__bases__)	#type的父类是object
print(type(1))			#1是int的实例

# 2.decorator
# 类装饰器
class ClassDecorator():
	def __init__(self):
		pass

	def __call__(self, func):
		def wrapper(*args, **kwargs):
			print("class decorator")
			return func(*args, **kwargs)
		return wrapper

@ClassDecorator()
def class_print():
	print("class print")
class_print()

# 函数装饰器
def func_decorator(para):
	def func_wrapper(func):
		def wrapper(*args, **kwargs):
			print(para)
			return func(*args, **kwargs)
		return wrapper
	return func_wrapper

@func_decorator("hello world")
def func_print():
	print("func print")
func_print()

# 3.classmethod staticmethod instancemethod
class PythonMethod(object):
	
	class_attr = "class attr"

	def __init__(self, idr, name, age):
		self._idr = idr
		self._name = name
		self.__age = age

	@property
	def idr(self):
		return self._idr

	@idr.setter
	def idr(self, idr):
		self._idr = idr

	@classmethod
	def class_method(cls):
		print("class_method:%s." % cls.class_attr)

	@staticmethod
	def static_method():
		print("static_method")

	def normal_method():
		print("normal_method")

	def __str__(self):
		return "PythonMethod__str__" # print(pm)调用

	def __repr__(self):
		return "PythonMethod__repr__" # >>>pm调用

	def __getattr__(self, key):
		print(self.__dict__[key])

	def __setattr__(self, key, value):
		self.__dict__[key] = value

pm = PythonMethod(1,"bao",12)
print(pm.idr)
pm.idr = 2
print(pm.idr)
pm.static_method()
pm.class_method()
PythonMethod.normal_method()
PythonMethod.static_method()
print(pm)
print(str(pm))
print(repr(pm))
setattr(pm,"name","cheng")
print(getattr(pm,"name"))

# 4.iterator generator closure
class Iterator(object):
	def __init__(self, count):
		self.i = 0
		self.count = count

	def __iter__(self):
		return self

	def __next__(self):
		if self.i < self.count:
			ret = self.i 
			self.i += 1
			return ret
		else:
			raise StopIteration() #for会对异常处理
for i in Iterator(3):
	print(i)

def odd():
	n = 1
	while True:
		yield n
		n += 2
odd_num = odd()
count = 0
for o in odd_num:
	if count>=5:
		break
	print(o)
	count += 1

class Odd():
	def __init__(self):
		self.start = -1
	def __iter__(self):
		return self
	def __next__(self):
		self.start += 2
		return self.start
O = Odd()
for i in range(5):
	print(next(O))



def closure():
	x = 1
	def inner():
		nonlocal x
		x += 1
		return x 
	return inner
func = closure()
print(func()) # 2
print(func()) # 3
print(func.__closure__)

func_list = []
for i in range(2):
	def func(x):
		return i*x 
	func_list.append(func)
for f in func_list:
	print(f(2))

func_list.clear()
for i in range(2):
	def make_func(i):
		def func(x):
			return i*x
		return func 
	func_list.append(make_func(i))
for f in func_list:
	print(f(2))

func = lambda x: x*x
for i in range(3):
	print(func(i))

# 5.装饰器注册函数

class FuncRegister():
	def __init__(self):
		self.callback = None

	def register(self, func):
		self.callback = func 

	def call(self):
		self.callback()

fr = FuncRegister()

@fr.register
def print_helloworld():
	print("hello world")

fr.call()  # hello world

class UrlHandlerReg():
	def __init__(self):
		self.handler_dict = {}

	def get(self, func):
		self.handler_dict["get"] = func 

	def post(self, method):
		def wrapper(func):
			self.handler_dict[method] = func 
		return wrapper

	def urlhandler_print(self):
		for k,v in self.handler_dict.items():
			print("%s:%s." %(k, v))

uhr = UrlHandlerReg()

@uhr.get
def get_handler():
	pass

@uhr.post("post")
def post_handler():
	pass

uhr.urlhandler_print()

# 6. subprocess asyncio threading multiprocessing 
import subprocess
ret = subprocess.call('dir',shell=True)
print(ret)

import os
import threading
import asyncio
async def hello():
	print("asyncio thread:%s" %(threading.currentThread()))
	r = await asyncio.sleep(1)
	print("asyncio thread:%s" %(threading.currentThread()))
loop = asyncio.get_event_loop()
tasks = [hello(),hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

tlock = threading.Lock()
def worker(sign, lock):
	lock.acquire()
	print("%s:%s" % (sign, os.getpid()))
	lock.release()
thread_list = []
for i in range(3):
	thread = threading.Thread(target=worker, args=('thread',tlock))
	thread_list.append(thread)
	thread.start()
for t in thread_list:
	t.join()

import platform
if 'Linux' in platform.platform():
	import multiprocessing
	plock = multiprocessing.Lock()
	process_list = []
	for i in range(3):
		process = multiprocessing.Process(target=worker, args=('process',plock))
		process_list.append(process)
		process.start()
	for p in process_list:
		p.join()

# 7.全局变量，局部变量，函数默认参数
start = 100
def tester(start):
	def nested(label):
		nonlocal start
		print(label, start)
		start += 3
	return nested
func = tester(100)
func(100) # 100 100 
print(start) # 100

def tester_global(start):
	def nested(label):
		global start
		print(label, start)
		start += 3
	return nested
func = tester_global(200)
func(100) # 100 100 
print(start) # 103

def function(para=[]):
	para.append(1)
	print(para)
function() # [1]
function() # [1,1] 
function() # [1,1,1]

def function(para=None):
	if para==None:
		para = []
	para.append(1)
	print(para)
function() # [1]
function() # [1]
function() # [1]

def function(count=0):
	count += 1
	print(count)
function() # 1
function() # 1 
function(2) # 3
function() # 1

# 8.map reduce filter

maps = [1,2,3]
new_maps = list(map(lambda x:x+1, maps))
print(new_maps) #[2,3,4]

import functools
new_reduces = functools.reduce(lambda x,y:x+y, maps)
print(new_reduces) # 6

new_filter = list(filter(lambda x: x>1 , maps))
print(new_filter) # [2,3]

# 9.logging
import logging
import sys
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(name)s:%(module)s:%(filename)s:%(funcName)s:%(lineno)d:%(message)s')
console_handler = logging.StreamHandler()
console_handler.formatter = formatter
file_handler = logging.FileHandler('python.log')
file_handler.formatter = formatter
logger = logging.getLogger("python")
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

logger.debug("hello world debug")
logger.info("hello world info")
logger.warning("hello world warning")
logger.error("hello world error")
logger.fatal("hello world fatal")

logging.basicConfig(format='%(asctime)s %(levelname)-8s:%(message)s', level=logging.DEBUG)
logging.debug('This message should go to the console')

import encodings
help(encodings)
print(sys.platform)
print(sys.getdefaultencoding())
print(sys.getsizeof(object))

# 10.opencv
import cv2
im = cv2.imread('./Koala.jpg')
print(im.shape)
h,w = im.shape[:2]
print(h,w)
cv2.imwrite('./Koala_new.png', im)

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
print(gray.shape)

