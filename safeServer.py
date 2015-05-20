from pyDes import *


class CSafeServer():
	"""DES encryption/decrytpion class"""
	KEY_MAP_SIZE = 256
	SAFE_KEY_LEN = 16
	m_mainKey = "amwfqp1121amwfqp"
	
	def __memset(self, mem, num, size):
		for i in xrange(size):
			mem[i] = chr(num)
			

	def __init__(self):
		keyLen = self.SAFE_KEY_LEN / 2;
		i = 0;
		self.m_keyMap = []
		key = [None] * keyLen;
		keyDes = triple_des(self.m_mainKey)
		while (i < self.KEY_MAP_SIZE):
			self.__memset(key, i, keyLen)
			i+= keyLen;
			encKey = keyDes.encrypt(''.join(key))
   			self.m_keyMap.extend(encKey)

	def test(self):
		print self.m_keyMap



if __name__ == '__main__':
    #_example_des_()
    #_example_triple_des_()

    
    safe_server = CSafeServer();
    safe_server.test();
