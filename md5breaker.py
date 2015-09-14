from urllib import request
import binascii

def reverseMD5(bytes):
  #this is the best bit so far
  h = binascii.hexlify(bytes)
  r = str(request.urlopen("https://duckduckgo.com/?q=md5+"+ str(h, "ascii") + "&ia=answer").read())
  p = posBehind(r, "result\":\"")
  return bytearray.fromhex(r[p:p+32])

def posBehind(str, x):
  return str.find(x) + len(x)

