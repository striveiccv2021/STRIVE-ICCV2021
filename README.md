
# STRIVE: Scene Text Replacement In Videos 

## Dataset Types:

* RoboText 
* SynthText
* RealWorld videos


***RoboText*** : Videos of texts collected using navigation robot in indoor environment. The overall duration of these videos is 10hrs+
Each text's background can be extracted from the bottom rectangle of its text rectangle.
The orginial unprocessed data is stored as RoboText-OriginalZip.7z.
Around 200 preprocessed videos are stored as RoboTextZip1.7z 

***SynthText*** : Using unity, we have created paired videos from synthetic scenes. These videos are stored with similar naming convention in drive.
File name : SynthText7Zip.7z

Note: Unity bbox are recorded as mirror values, hence the bbox extraction process will be different than other two video types.

***Real World videos***: We have collected videos using high resolution mobile camera to capture texts in different lighting conditions and motion blur.
File name: RealWorld.7z

## Preparing data
We have extracted text bounding box from RoboText and Real world videos using AWS Rekognition API. The code available as runAWS.py file.
Synthetic videos bbox is recorded in unity environment

## Data Preprocessing

Refer to the preprocessing python file for each dataset type to get crop images of text.

# Data download

Data can be downloaded from [here](https://drive.google.com/drive/folders/1sCekCP3seKxBSGC2Uk9DiCywDWOjRCu-?usp=sharing) 

