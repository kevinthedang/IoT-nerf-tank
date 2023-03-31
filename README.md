# IoT Nerf Tank

## Table of Contents
* [Description](#description)
* [Libraries](#libraries--modules)
* [To Run](#to-run--test)
* [Commands](#commands)
* [Parts](#parts)
* [Credit](#credit)
* [License](#license)

## Description
For this project, we were inspired to combine a tank chassis with a nerf turret to create a tank that will be connected to a web server. The server will send json messages to certain topics on AWS where the tank (Raspberry Pi) will receive the messages through a proxy and execute the parsed commands.

## Libraries / Modules
* Front-End
    * [React](https://react.dev/)
    * [Vite](https://vitejs.dev/)
    * [Axios](https://axios-http.com/docs/intro)
* Back-end
    * [aws-iot-device-sdk](https://github.com/aws/aws-iot-device-sdk-js)
    * [Cors](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
    * [Express](http://expressjs.com/en/starter/installing.html)
* AWS-Tank Proxy:
    * [awscrt](https://pypi.org/project/awscrt/)
    * command_line_utils.py
        * [awsiot-python-sdk](https://github.com/aws/aws-iot-device-sdk-python-v2)
            * `mqtt_connection_builder.py` (should be in the `awsiot` directory)
                * If there is a error on call, the proxy could also depend on `mqtt5_client_builder.py`
* Tank Controller
    * [RPI.GPIO](https://pypi.org/project/RPi.GPIO/)
    * [gpiozero](https://pypi.org/project/gpiozero/)
    * [paho-mqtt](https://pypi.org/project/paho-mqtt/)

## To Run / Test
* Get the [SDK](https://github.com/aws/aws-iot-device-sdk-python) onto the pi and have certificates ready from aws to run commands to the pi from the client
    * create folder in the `~` directory called `certs` and place all of your certification files in there.
    * You will need to run a certain command in the `ClientToJoxConnectionProxy` directory.
        * `python3 internetJox.py --topic <your topic-name> --ca_file ~/certs/AmazonRootCA1.pem --cert ~/certs/certificate.pem.crt --key ~/certs/private.pem.key --endpoint <your aws endpoint here>`
            * You can also you the topic that the server uses: `from_client`.
    * You will also need to run another command in a seperate terminal called `RobotJoxControl.py` can be found in the `RobotJoxControl` directory
        * Run the file as `./RobotJoxControl.py`.
    * Now the Tank should be able to listen to outside commands:
        * Jox <--- AWSProxy <--- ExternalClient(s)...
    * `internetJox.py` is not required for any other type of control or connection you would like to make with the tank! It is only a sample of a connection from a separate (or same) network client.

    
* Pull client and server [code](https://github.com/kevinthedang/IoT-nerf-tank) directories
    * You will need to add your certifications into the `server` directory as a folder named `certifs`
    * You will also need a json file named `endpoint.json` to hold your endpoint for the server to connect to:
        * i.e. `{ "endpoint": "<your_endpoint_here>" }`
    * NodeJs must be install to run the client and sever
        * go into the `client` directory and run `npm i` then `npm start`
        * go into the `server` directory and run `npm i` then `npm start`
        * not the server should be up at `localhost:5173` most likely (or whatever vite tells you its hosted at)
    * Now you can click on the buttons and the Pi should receive the messages!
    * Jox <--- AWSProxy <--- ExpressClient <---> UserClient

## Commands
* There are not too many commands for the Tank to run, but knowing them can help customize how they can run (either from the proxy or from default calls)
    * Treads:
        * "leftTread:drive:`<value between -1 to 1>`"
        * "rightTread:drive:`<value between -1 to 1>`"
    * Turret: 
        * To fire the turret, call commands in order:
            * "flywheel:fire"
            * "ammoRammer:fire"
        * Turret Elevation:
            * "gunElevator:`<"up" or "down">:`:`<degrees>`"
                * The current degrees cannot exceed 90
        * Turret Left / Right:
            * "turretRing:`<"turnRight" or "turnLeft">`:`<degrees>`"
                * The current degrees cannot exceed 90
        * Targeting Laser:
            * "targetingLaser:`<"on" or "off">`"
        * Some commands can be set to 0 degrees (home angle):
            * "`<"gunElevator" or "turretRing">`:setHome"


## Parts
* Refer to: 
    * `Parts_List.xlsx` in the `extras` folder for all the turret parts bought
    * [Bluetooth Nerf Turret - Hardware](https://www.littlefrenchkev.com/bluetooth-nerf-turret/#comp-k1tpv8jv)
    * [SZDoit Black T300 Tank Chassis](https://www.amazon.com/SZDoit-Raspberry-Learning-Caterpillar-Platform/dp/B08HRTZNHW/ref=sr_1_1?crid=G1VU0HSPKZJ4&keywords=tank+chassis+SZDoit+Black+T300+Robot+tracked+car+for+Arduino%2FRaspberry+pi&qid=1676065310&refinements=p_n_availability%3A2661601011&rnid=2661599011&s=toys-and-games&sprefix=tank+chassis+szdoit+black+t300+robot+tracked+car+for+arduino%2Fraspberry+p%2Ctoys-and-games%2C113&sr=1-1) (Alternative and cheaper options for chassis are fine too)
    * [Raspberry Pi](https://www.adafruit.com/product/4296)
    * Also Refer to `3D printing parts` for other parts to for mounting
    * [Adafruit DC and Stepper Motor HAT for Raspberry Pi](https://www.adafruit.com/product/2348)
        * [Documentation](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-dc-motors) for use

## Credit
* [Kole Davis](https://github.com/Kole0518)
* [Drew Bogdan](https://github.com/DrewBogdan)
* [Vincent Do](https://github.com/VinnyVinVince)
* [Kevin Dang](https://github.com/kevinthedang)
* [Aaron Crandall](https://github.com/acrandal)

## License
MIT License

Copyright (c) 2023 Kevin Dang, Drew Bogdan, Vincent Do, Kole Davis, Aaron Crandall

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.