import random

def get_token():
	t=random.randint(1,4)
	# if t==0 :
	# 	token='52e9a368958cc817e8e82c8d9aca8304346e48b25ed01f92b649e7ad' 
	# elif t==1:
	# 	token='6b6eab34ea42bcdb84161e8993950a73e82f756d2d054682dfe05582' 
	# else:
	# 	token='4ceed8325987d078ede9c37f94c46ec805cb064773d541f42a7ee72a' 
	token='52e9a368958cc817e8e82c8d9aca8304346e48b25ed01f92b649e7ad' 
		
	return token
if __name__ == '__main__':
	print(get_token())



