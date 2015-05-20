# -*- coding:utf-8 -*-  

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

	def getRealKey(self, keyInf, keyInfLen, pKey):
		keyLen = self.SAFE_KEY_LEN;
		if keyInfLen != self.KEY_INF_LEN:
			return ;

		realKeyInf = []
		keyDes = triple_des(self.m_mainKey)
		#解密keyInf
		i = 0;
		while (i < self.KEY_INF_LEN):
			decKeyInf = keyDes.decrypt(''.join(keyInf[i:i+keyLen]))
			realKeyInf.extend(decKeyInf)
			i += keyLen;

		#获取主密钥
		
		#pos = 0
		#mainKeyIndexs = realKeyInf + pos

		pass

	def __decode(self, keyInf, keyInfLen, pSrc, srcLen, pDst):
		if keyInfLen != self.KEY_INF_LEN:
			return 

		realKey = []
		self.getRealKey(keyInf, keyInfLen, realKey)

		pass
	def createAccessRep(self, access, accessLen):
		keyInf = self.getAccessKeyInf()
		print keyInf
		accessRep = []
		self.__decode(keyInf, self.KEY_INF_LEN, access, accessLen, accessRep)

		return accessRep

	def test(self):
		print self.m_keyMap
		print self.KEY_INF_LEN



if __name__ == '__main__':
    #_example_des_()
    #_example_triple_des_()

    
    safe_server = CSafeServer();

    safe_server.createAccessRep("12", 16)
