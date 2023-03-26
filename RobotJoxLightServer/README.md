# Robot Jox Light Server for RGB LED strip

System service for controlling the RGB LED light strip.
It listens on an MQTT topic for control messages and runs the strip from those.
See message options and formats below for documentation.

See Makefile for install, dependencies, and service start/stop controls.

### MQTT settings:

- host: localhost  
- topic: lights

### Message types and formats:

- "blankLights"
    - Will blank out (turn off) the whole strip

- "setPixel"
    - Sets a single pixel a provided RGB color
    - index: pixel strip led index
    - R,G,B: values of 0..255 for the light values to set the pixel
    - format: "setPixel:index:R:G:B"
    - example: "setPixel:3:150:150:0"
