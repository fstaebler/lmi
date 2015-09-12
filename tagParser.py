import struct
import bitstruct
import sys
import imageSaver as imgS
targetFile = sys.argv[1]

def parseTag(tagType, tagData):
  try:
    tagName = ({'45': 'SoundStreamHead2', '10': 'DefineFont', '21': 'DefineBitsJPEG2', '14': 'DefineSound', '36': 'DefineBitsLossless2', '91': 'DefineFont4', '39': 'DefineSprite', '64': 'EnableDebugger2', '71': 'ImportAssets2', '15': 'StartSound', '9': 'SetBackgroundColor', '23': 'DefineButtonCxform', '26': 'PlaceObject2', '6': 'DefineBits', '18': 'SoundStreamHead', '5': 'RemoveObject', '34': 'DefineButton2', '93': 'EnableTelemetry', '74': 'CSMTextSettings', '33': 'DefineText2', '57': 'ImportAssets', '4': 'PlaceObject', '17': 'DefineButtonSound', '82': 'DoABC', '87': 'DefineBinaryData', '83': 'DefineShape4', '75': 'DefineFont3', '58': 'EnableDebugger', '88': 'DefineFontName', '48': 'DefineFont2', '59': 'DoInitAction', '32': 'DefineShape3', '56': 'ExportAssets', '89': 'StartSound2', '90': 'DefineBitsJPEG4', '22': 'DefineShape2', '66': 'SetTabIndex', '13': 'DefineFontInfo', '70': 'PlaceObject3', '35': 'DefineBitsJPEG3', '11': 'DefineText', '12': 'DoAction', '78': 'DefineScalingGrid', '46': 'DefineMorphShape', '65': 'ScriptLimits', '24': 'Protect', '8': 'JPEGTables', '76': 'SymbolClass', '2': 'DefineShape', '7': 'DefineButton', '0': 'End', '43': 'FrameLabel', '86': 'DefineSceneAndFrameLabelData', '28': 'RemoveObject2', '1': 'ShowFrame', '73': 'DefineFontAlignZones', '19': 'SoundStreamBlock', '69': 'FileAttributes', '37': 'DefineEditText', '84': 'DefineMorphShape2', '61': 'VideoFrame', '20': 'DefineBitsLossless', '60': 'DefineVideoStream', '77': 'Metadata', '62': 'DefineFontInfo2'}[str(tagType)]) #lol parser
  except:
    print("Non-Standard Tag Type: " + str(tagType))
    return False
  try:
    return {"TagName": tagName, "TagContent": eval("parse" + tagName + "(tagData)")}
  except NameError:
    print("Failed Parsing " + tagName + " Tag!")
    return False
#def parseFileAttribute(tagData):
#  print("FileAttribute Tag.")
#  print("")

def parseSetBackgroundColor(tagData):
  #SetBackgroundColor Tag - Contains the background color.
  return{"R": tagData[0], "G": tagData[1], "B": tagData[2]}
#def parseEnableDebugger2(tagData):
#  print("EnableDebugger2 Tag.")
#  print("")
def parseShowFrame(tagData):
  #ShowFrame Tag - Has no specified data.
  return {}
def parseEnd(tagData):
  #End Tag - Has no specified data.
  return {}
#def parseImportAssets2(tagData):
#  print("ImportAssets2 Tag.")
#  print("")
#def parseDefineShape(tagData):
#  print("DefineShape Tag.")
#  print("")
#def parseDefineSprite(tagData):
#  print("DefineSprite Tag.")
#  print("")
def parseSymbolClass(tagData):
  #SymbolClass Tag - Creates associations between symbols in the SWF file and ActionScript 3.0 classes
  numSymbols = struct.unpack("<H", tagData[0:2])[0]
  r = {"numSymbols" : numSymbols, "symbols" : []}
  cursor = 2
  while cursor < len(tagData):
    symbolID = struct.unpack("<H", tagData[cursor:cursor+2])[0]
    cursor +=2
    symbolName = []
    while True:
      x = tagData[cursor]
      cursor +=1
      if(x == 0):
        break
      symbolName += [x]
    symbolName = str(bytearray(symbolName), "ascii")
    r["symbols"] += [{"ID": symbolID, "Name": symbolName}]
  return r
def parseDefineBitsLossless(tagData):
  characterId = struct.unpack("<H", tagData[0:2])[0]
  bitmapFormat = tagData[2]
  bitmapWidth = struct.unpack("<H", tagData[3:5])[0]
  bitmapHeight = struct.unpack("<H", tagData[5:7])[0]
  if (bitmapFormat == 3):
    cursor = 8
    tableSize = tagData[7] + 1
  else:
    cursor = 7
    tableSize = 0
  bitmapPath = imgS.bitsLossless(tagData[cursor:], bitmapFormat, bitmapWidth, bitmapHeight, tableSize, targetFile + ".characters." + str(characterId))
  return {"CharacterId": characterId,
          "BitmapFormat": bitmapFormat,
          "bitmapWidth": bitmapWidth,
          "bitmapHeight": bitmapHeight, 
          "bitmapData": bitmapPath}
def parseDefineBitsLossless2(tagData):
  characterId = struct.unpack("<H", tagData[0:2])[0]
  bitmapFormat = tagData[2]
  bitmapWidth = struct.unpack("<H", tagData[3:5])[0]
  bitmapHeight = struct.unpack("<H", tagData[5:7])[0]
  if (bitmapFormat == 3):
    cursor = 8
    tableSize = tagData[7] + 1
  else:
    cursor = 7
    tableSize = 0
  bitmapPath = imgS.bitsLossless(tagData[cursor:], bitmapFormat + 10, bitmapWidth, bitmapHeight, tableSize, targetFile + ".characters." + str(characterId))
  return {"CharacterId": characterId, 
          "BitmapFormat": bitmapFormat, 
          "BitmapWidth": bitmapWidth,
          "BitmapHeight": bitmapHeight,
          "BitmapData": bitmapPath}
def parseDefineSound(tagData):
  characterId = struct.unpack("<H", tagData[0:2])[0]
  formatRateSizeType = bitstruct.bytesToBits([tagData[2]])
  soundFormat = bitstruct.bitsToUInt(formatRateSizeType[0:4])
  soundRate = bitstruct.bitsToUInt(formatRateSizeType[4:6])
  if formatRateSizeType[6]:
    soundSize = 16
  else:
    soundSize = 8
  soundStereo = formatRateSizeType[7]
  return {"CharacterId": characterId,
          "SoundFormat": soundFormat,
          "SampleRate": [5512, 11025, 22050, 44100][soundRate],
          "SampleSize": soundSize,
          "Stereo":soundStereo
         }