from csv import DictReader
from PIL import Image, ImageDraw, ImageFont
import os
import sys
import math


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in DEGREES.
    """

    angle = angle/57.2958
    ox, oy = origin
    px, py = point

    qx = int(ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy))
    qy = int(oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy))
    return qx, qy


jsonfile = sys.argv[1]
pngspath = "pngs"
mp4path = "mp4s"
os.mkdir(pngspath)
if not os.path.isdir(mp4path):
    os.mkdir(mp4path)
# open file in read mode
with open(jsonfile, 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_dict_reader = DictReader(read_obj)
    clock = 0
    imgnum = 0
    # Iterate over each row in the csv using reader object
    for row in csv_dict_reader:
        
        # row variable is a list that represents a row in csv
       # print(row)
        if int(float(row["cts"])) > clock+200 :
            clock = int(float(row["cts"]))
            digitimg = Image.new('RGB', (200, 100), color = (0, 0, 0))
            d = ImageDraw.Draw(digitimg)
            speed = int(float(row["GPS (2D speed) [m/s]"])*2.23694)
            fnt = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 50)
            d.text((10,10), str(speed) + " mph" , font=fnt,fill=(255,255,0))

            img = Image.open('speedo.png')

            imgline = ImageDraw.Draw(img)
            shape=[(132,163),(251,163)] # 20mph
            origin=(226,165)
            #mph = 125
            angle = -31 + (1.57895*speed)
            newlineshape=(rotate(origin,shape[0],angle),rotate(origin,shape[1],angle))
            imgline.line(newlineshape,fill="red",width=4)
            #img.save("testimage.png" )
            img.save(pngspath+"/img"+"{:0>4d}".format(imgnum) +".png" )
            digitimg.save(pngspath+"/digitimg"+"{:0>4d}".format(imgnum) +".png" )
            imgnum=imgnum+1
        else:
            continue
ffmpeg1command = "ffmpeg -r 5 -i \""+pngspath+"/img%04d.png\" -c:v libx264 -vf fps=5 -pix_fmt yuv420p \""+mp4path+"/" + jsonfile + ".mp4\"" 
print (ffmpeg1command)
os.system(ffmpeg1command)
ffmpeg2command = "ffmpeg -r 5 -i \""+pngspath+"/digitimg%04d.png\" -c:v libx264 -vf fps=5 -pix_fmt yuv420p \""+mp4path+"/" + jsonfile + "_digit.mp4\"" 
print (ffmpeg2command)
os.system(ffmpeg2command)

onlyfiles = [f for f in os.listdir(pngspath) if os.path.isfile(os.path.join(pngspath, f))]
for file in onlyfiles:
    os.remove(pngspath + "/" + file)
os.rmdir(pngspath)
    
