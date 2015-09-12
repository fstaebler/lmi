import sys
print("Legacy Media Inspector")
if len(sys.argv) < 2:
  print("Usage: python3 lmi.py <filename> [options]")
  exit()
targetFile = sys.argv[1]

import struct
import bitstruct
import lzma
import zlib
import tagParser as tp
import json

f = open(targetFile, "rb");

###Header Parsing
#Type, Version, Size
swfType = f.read(3);
swfVersion = struct.unpack("<B", f.read(1))[0]
swfLength = struct.unpack("<I", f.read(4))[0]

#Decompress
if swfType == b'ZWS':
  print("Decompressing using lzma...")
  swfData = lzma.decompress(f.read())
elif swfType == b'CWS':
  print("Decompressing using zlib...")
  swfData = zlib.decompress(f.read())
elif swfType == b'FWS':
  print("Loading...")
  swfData = f.read()
else:
  print("Not an SWF file!")
  exit()
seekPosition = 0

print("SWF Version " + str(swfVersion))
print("")

#size of the Frame
shift, swfFrameSize = bitstruct.unpackRECT(swfData[:17])
seekPosition += shift

#Framerate and -count
swfFrameRate = swfData[seekPosition] / 256 + swfData[seekPosition+1]
seekPosition += 2
swfFrameCount = struct.unpack("<H", swfData[seekPosition:seekPosition+2])[0]
seekPosition += 2

print("Frame Size (Twips): " +  str(swfFrameSize))
print("Duration (Frames): " + str(swfFrameCount))
print("Frame Rate: " +  str(swfFrameRate))
print("")

###Tag Parsing

tags = []
while seekPosition < len(swfData):
  #Extract Tag Headers
  thisTagHeader = struct.unpack("<H", swfData[seekPosition:seekPosition+2])[0]
  seekPosition += 2
  #Parse Tag Headers
  thisTagType = (thisTagHeader >> 6) & (2 ** 10 - 1)
  thisTagSize = thisTagHeader & (2 ** 6 - 1)
  if (thisTagSize == 0x3f):
    thisTagSize = struct.unpack("<I", swfData[seekPosition:seekPosition+4])[0]
    seekPosition += 4
  
  thisTagParserResult = tp.parseTag(thisTagType, swfData[seekPosition:seekPosition+thisTagSize])
  if(thisTagParserResult):
    tags += [thisTagParserResult]
  seekPosition += thisTagSize

open(targetFile + ".json", "a").close()
f = open(targetFile + ".json", "w")
f.write(json.dumps(tags, indent=2, sort_keys=True))
f.close()
