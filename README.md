# lmi
## legacy media inspector
#### parse swf files as specified by adobe

Usage:
```
$ python3 lmi.py swf-file-you-want-to-inspect.swf
```

#### look at the data inside the file

lmi exports the image content of `DefineBitsLossless` and other tags as image files. The files are named after the character IDs, like this:
```
$ python3 lmi.py path/swf-file.swf
$ ls path
swf-file.swf
swf-file.swf.characters.3.png
swf-file.swf.characters.15.png
swf-file.swf.characters.19.png
swf-file.swf.json
```
The JSON file contains an array of all tags, in the original order and with all information contained in each tag.

#### this project is far from finished

Right now, lmi only parses very few tags.

##### Supported Tags
* SetBackgroundColor
* ShowFrame
* End
* SymbolClass
* DefineBitsLossless2

Partially supported:
* DefineSound - No actual sound data is exported.
* DefineBitsLossless
* DefineShape
* DefineShape2
* DefineShape3
* DefineShape4