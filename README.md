# Memify

An app to turn yourself (or anyone for that matter) into a meme. It takes in a live webcam feed and displays the current locations of everyone’s facial features. When satisfied, press the relevant key (eg. p for thug lyf) to turn yourself into the meme.

Uses OpenCV, numpy and a bit of command line stuff (ffmpeg).

How to add a meme:

1. Create a function for the meme.
  1. Declare function with the shown parameters  
def meme1(frame,faces,mouths,eyes)
  2. Import images.  
Currently done using cv2.imread()
  3. Place the image over the frame.  
Currently done using numpy
  4. Export the frame if wanted.  
Currently done using cv2.imwrite()
  5. Return the frame.
2. Follow code for thug lyf in capVideo(), adding an else if statement)