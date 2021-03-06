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

	def getRealKey(self, keyInf, keyInfLen):
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

		pos = 0
		mainKey = []
		#获取主密钥
		i = 0
		while (i < keyLen):
			mainKey.extend(self.m_keyMap[ord(realKeyInf[i+pos])])
			i += 1
		pos += keyLen;
		#获取密钥索引映射表:先用主密钥解密，再用m_keyMap 映射回来	
		keyMapIndexs = []
		realKeyMap = []
		mainKeyDes = triple_des(''.join(mainKey))
		i = 0
		while (i < self.KEY_MAP_SIZE):
			decRealKeyInf = mainKeyDes.decrypt(''.join(realKeyInf[i+pos:i+pos+keyLen]))
			keyMapIndexs.extend(decRealKeyInf)
			i+= keyLen;

		i = 0
		while (i < self.KEY_MAP_SIZE):
			realKeyMap.extend(self.m_keyMap[ord(keyMapIndexs[i])])
			i += 1

		pos += self.KEY_MAP_SIZE;
		#获取实际密钥
		realKeyIndexs = []
		
		decRealKeyIndexs = mainKeyDes.decrypt(realKeyInf[pos:pos+keyLen])

		i = 0
		while (i < keyLen):
			realKeyIndexs.extend(self.m_keyMap[ord(decRealKeyIndexs[i])])
			i += 1

		realKey = []
		i = 0
		while (i < keyLen):
			realKey.extend(realKeyMap[ord(realKeyIndexs[i])])
			i += 1
		pos += keyLen;

		return realKey

	def __decode(self, keyInf, keyInfLen, pSrc, srcLen):
		if keyInfLen != self.KEY_INF_LEN:
			return 

		realKey = []
		realKey = self.getRealKey(keyInf, keyInfLen)

		realKeyDes = triple_des(''.join(realKey))
		
		decSrc = realKeyDes.decrypt(pSrc[:srcLen])
		return decSrc

	def createAccessRep(self, access, accessLen):
		keyInf = self.getAccessKeyInf()
		decAccessRep = self.__decode(keyInf, self.KEY_INF_LEN, access, accessLen)

		accessRep = []
		i = 0
		while (i < accessLen):
			accessRep.extend(self.m_accessMap[ord(decAccessRep[i])])
			i += 1

		return accessRep

	def test(self):
		print self.m_keyMap
		print self.KEY_INF_LEN


def main():
    if len(sys.argv) != 2:
    	return  
    access = sys.argv[1]
    accessLen = len(sys.argv[1])
    
    if accessLen != 8 :
    	return 

    safe_server = CSafeServer()
    print safe_server.createAccessRep(''.join(access), accessLen)

if __name__ == '__main__': 
	main()

