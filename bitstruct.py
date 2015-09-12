import math
#this whole thing is a bit tricky. as some idiot at adobe decided to make up
#weird binary formats that span across bytes, we have to decode those now.

def bytesToBits(bytes):
  #does exactly what the name says. bits as booleans, big endian
  result = []
  for b in bytes:
    for s in range(8):
      result += [b & 1 << (7 - s) == 1 << (7 - s)]
  return result
  
def bitsToUInt(bits):
  result = 0
  s = len(bits) - 1
  for b in bits:
    if b:
      result += 1 << s
    s -= 1
  return result 
  
def bitsToInt(bits):
  result = 0
  s = len(bits) - 2
  if bits[0]:
    result -= 1 << (s + 1)
  for b in bits[1:]:
    if b:
      result += 1 << s
    s -= 1
  return result 
  
def bLength(bits):
  return math.ceil(bits/8)

def unpack(format, data):
  #format description:
  # "Un" = Unsigned int, n bit
  # "Sn" = Signed int, n bit
  # "Fn" = Fixed point, n bit
  # "xn" = Ignore n bits
  # n has to be padded with a 0 if only one char
  # will fill with zeroes if data is insufficient.
  return (0)
  
def unpackRECT(data):
  dataBits = bytesToBits(data)
  uintSize = bitsToUInt(dataBits[:5])
  rectSize = bLength(5 + uintSize * 4)
  xMin = bitsToInt(dataBits[5:5+uintSize])
  xMax = bitsToInt(dataBits[5+uintSize:5+2*uintSize])
  yMin = bitsToInt(dataBits[5+uintSize*2:5+3*uintSize])
  yMax = bitsToInt(dataBits[5+uintSize*3:5+4*uintSize])
  return (rectSize, (xMin, yMin, xMax, yMax))
def unpackRGB15(data):
  dataBits = bytesToBits(data)
  r = bitsToUInt(dataBits[1:6])
  g = bitsToUInt(dataBits[6:11])
  b = bitsToUInt(dataBits[11:])
  return(r, g, b)
