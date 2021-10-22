import argparse
import os
import shutil
import cv2


def extractImages(pathIn, pathOut):

    if os.path.exists(pathOut):
        # delete dir
        shutil.rmtree(pathOut) 

    if not os.path.exists(pathOut):
        # create dir
        os.makedirs(pathOut)
    
    count = 0
    cap = cv2.VideoCapture(pathIn)

    while True:
        cap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
        success, image = cap.read()
        
        if success is True:
            print (f'Read a frame {count}: ', success)
            cv2.imwrite(pathOut + f"\\frame{count}.jpg", image)  # save frame as JPEG file
            count += 1
        else:
            print("------END------")
            break
       


parser = argparse.ArgumentParser(description="Convert video to photos")

parser.add_argument("-i", "--pathIn", help="path to video")
parser.add_argument("-o", "--pathOut", help="path to images")

args = parser.parse_args()

# print(args.pathIn)

if args.pathOut is None:
    args.pathOut =  os.path.split(os.path.abspath(args.pathIn))[0] + "\photos_with_video"

# print(args.pathOut)
# print(os.path.split(os.path.abspath(args.pathIn))[0])

# count = 0
# print(args.pathOut + f"\\frame{count}.jpg")


extractImages(args.pathIn, args.pathOut)



