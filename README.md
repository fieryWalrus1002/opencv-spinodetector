# opencv-spinodetector
A small python script to detect errant blue Lego dinosaur heads lost in your yard.

Have you ever lost a Lego dinosaur head with a sky blue coloration in a yard with long
grass? Well, you're in luck! With the power of OpenCV and Python, you can increase
the odds of discovering the errant cretaceous cranium with this Spino-Detector!

You'll need:
- a pc to run the Python script
- OpenCv installed
- a webcam taped to a stick(1)

Simply activate the spino-detector with the command:
'python -m spino-detector.py -cam=0'

To exit, hit Escape. To save a picture, hit spacebar.

Now you can scan your local area for possible dinosaur hiding spots. Possible locations
are marked with magenta boxes. If your dinosaurs are of a different color, you can use 
specify that color with the argument '-color <colorname>'. The only color available
is skyblue, so I hope your dinosaur is that color. 

You can also specify the color of the bounding box by passing '-bbcolor="0, 244, 2"' or
any such BGR values.

If you have multiple web cams, you can add the argument '-cam=#', where # is an integer.
Zero would be your built-in webcam on a laptop, and usb web cams would be either 1 or 2.
Mine was 2. 

(1) While this isn't strictly necessary, but our highly-trained dinosaur experts maintain that
a proper spino-detector be equipped with a long handle and a flashlight for safety
purposes. Dinosaurs have sharp teeth!
