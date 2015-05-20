from pyDes import *


class CSafeServer():
	"""DES encryption/decrytpion class"""
	KEY_MAP_SIZE = 256
	SAFE_KEY_LEN = 16
	KEY_INF_LEN = KEY_MAP_SIZE + SAFE_KEY_LEN*2
	m_mainKey = "amwfqp1121amwfqp"
	m_accessMap = [None] * KEY_MAP_SIZE;
	m_keyMap = []

	def __memset(self, mem, num, size):
		for i in xrange(size):
			mem[i] = chr(num)
			

	def __init__(self):
		keyLen = self.SAFE_KEY_LEN / 2;
		i = 0;
		key = [None] * keyLen;
		keyDes = triple_des(self.m_mainKey)
		while (i < self.KEY_MAP_SIZE):
			self.__memset(key, i, keyLen)
			i+= keyLen;
			encKey = keyDes.encrypt(''.join(key))
   			self.m_keyMap.extend(encKey)

		keyArray = "qwertyuiopasdfghjklzxcvbnm";
		for i in xrange(self.KEY_MAP_SIZE):
			self.m_accessMap[i] = keyArray[ord(self.m_keyMap[i])%26];

	def getAccessKeyInf(self):
		keyInf = ['\x11'] * self.KEY_INF_LEN;
		for i in xrange(self.KEY_MAP_SIZE):
			keyInf[i] = self.m_keyMap[i];
		return keyInf

	def createAccessRep(self, access, accessLen):

		return accessRep

	def test(self):
		print self.m_keyMap
		print self.KEY_INF_LEN



if __name__ == '__main__':
    #_example_des_()
    #_example_triple_des_()

    
    safe_server = CSafeServer();
    safe_server.getAccessKeyInf()
