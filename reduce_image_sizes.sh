# Put all images in the current path in a directory called images
# Tested on: macOS Monterey

mkdir -p processed/images
for f in images/*.jpg images/*.png images/*.jpeg
 do
        ffmpeg -i $f -q:v 10 processed/$f -y
done
