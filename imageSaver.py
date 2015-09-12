import zlib
import sys
import bitstruct
import math
from PIL import Image

def bitsLossless(data, imgformat, width, height, tableSize, path):
  data = zlib.decompress(data)
  #TODO: Replace PIL.Image.putpixel with a faster alternative!
  if imgformat == 3: #RGB 8-Bit Indexed
    i = Image.new("RGB", (width, height))
    paddedWidth = 4 * math.ceil(width / 4)
    lut = data[0:tableSize * 3]
    imd = data[tableSize * 3:]
    for x in range(paddedWidth):
      for y in range(height):
        if x < width:
          v = imd[y*paddedWidth + x]
          c = (lut[v * 3], lut[v * 3 + 1], lut[v * 3 + 2])
          i.putpixel((x,y), c)
  elif imgformat == 13: #RGBA 8-Bit Indexed
    i = Image.new("RGBA", (width, height))
    paddedWidth = 4 * math.ceil(width / 4)
    lut = data[0:tableSize * 4]
    imd = data[tableSize * 4:]
    for x in range(paddedWidth):
      for y in range(height):
        if x < width:
          v = imd[y*paddedWidth + x]
          c = (lut[v * 4], lut[v * 4 + 1], lut[v * 4 + 2], lut[v * 4 + 3])
          i.putpixel((x,y), c)
  elif imgformat == 15: #ARGB Full-Color
    i = Image.new("RGBA", (width, height))
    for x in range(width):
      for y in range(height):
        j = (y * width + x) * 4
        c = (data[j + 1], data[j + 2], data[j+3], data[j])
        i.putpixel((x,y), c)
  elif imgformat == 4:
    fac = (2 ** 8 - 1) / (2 ** 5 - 1)
    paddedWidth = 2 * math.ceil(width / 2)
    for x in range(paddedWidth):
      for y in range(height):
        if x < width:
          c = bitstruct.unpackRGB15(data[(y*paddedWidth + x) * 2])
          c = (8 * c[0], 8 * c[1], 8 * c[2])
          i.putpixel((x,y), c)
  elif imgformat == 5:
    pass
  else:
    print(str(imgformat))
    print("not implemented!")
  i.save(path + ".png")
  return path + ".png"