# Makes a simple speedo (needle and digits style) from GoPro metadata

## What?
Takes a GoPro GPS CSV made on https://goprotelemetryextractor.com/free/ and makes a speedo video to use in video editing software. Very primitive.
Requires FFmpeg (I assume it's on your PATH).
Made for Windows, you may have to adjust the font path for other OS.

## Cams?
Made for my GoPro Hero 8 BLACK where it works very well although I only have basic Python experience (I don't know what I'm doing).

## Usage
`python makevideo.py "2022.04.15.16.38.47 GX031416_HERO8 Black-GPS5.csv"`

## How it works?
Creates a png for every video frame in ./pngs/ then uses FFmpeg to make videos from them.

## Output
Creates 2 mp4 files in ./mp4s/ which you can use in video editing software.
