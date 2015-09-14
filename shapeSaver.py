import bitstruct
import struct

def unpackGRADIENT(data):
  dataBits = bitstruct.bytesToBits([data[0]])
  spreadMode = ["Pad", "Reflect", "Repeat", False][bitstruct.bitsToUInt(dataBits[0:2])]
  interpolationMode = ["Normal", "Linear", False, False][bitstruct.bitsToUInt(dataBits[2:4])]
  numGradients = bitstruct.bitsToUInt(dataBits[4:])
  gradientRecords = []
  for index in range(numGradients):
    gradientRecords += [{"Ratio":data[index * 4 + 1],
                         "R":data[index * 4 + 2],
                         "G":data[index * 4 + 3],
                         "B":data[index * 4 + 4]}]
  return numGradients * 4 + 1, {"SpreadMode":spreadMode,
                                "InterpolationMode":interpolationMode,
                                "GradientRecords":gradientRecords}

def defineShape(data, version):
  fillStyleCount = data[0]
  if (fillStyleCount == 0xff) and ((version == 2) or (version == 3)):
    fillStyleCount = struct.unpack("<H", data[1:3])[0]
    print("long")
    cursor = 3
  else:
    cursor = 1
  fillStyles = []
  parsedStyles = 0
  while (fillStyleCount > 0) and (parsedStyles < fillStyleCount): #parse fillstylearray
    thisStyle = {}
    thisStyle["FillStyleType"] = data[cursor]
    cursor += 1
    if thisStyle["FillStyleType"] == 0x00: #solid fill
      thisStyle["Color"] = {"R": data[cursor], #rgb color
                            "G": data[cursor+1],
                            "B": data[cursor+2]}
      cursor += 3
      if version == 3: #rgba color
        thisStyle["Color"]["A"] = data[cursor]
        cursor += 1
    elif thisStyle["FillStyleType"] in [0x10, 0x12, 0x13]: #gradient fill
      offset, thisStyle["GradientMatrix"] = bitstruct.unpackMATRIX(data[cursor:])
      cursor += offset
      offset, thisStyle["Gradient"] = unpackGRADIENT(data[cursor:])
      cursor += offset
    elif thisStyle["FillStyleType"] in [0x40, 0x41, 0x42, 0x43]: #bitmap fill
      thisStyle["BitmapId"] = struct.unpack("<H", data[cursor:cursor+2])[0]
      offset, thisStyle["BitmapMatrix"] = bitstruct.unpackMATRIX(data[cursor+2:])
      cursor += 2 + offset
    parsedStyles +=1
    fillStyles += [thisStyle]
  lineStyles = False
  shapeRecords = False

  return fillStyles, lineStyles, shapeRecords

def defineShape4(data):
  return False, False, False
