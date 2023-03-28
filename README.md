# IoT Nerf Tank

## Table of Contents
* [Description](#description)
* [Software Used](#software-used)
* [Parts](#parts)
* [Credit](#credit)
* [License](#license)

## Description
For this project, we were inspired to combine a tank chassis with a nerf turret to create a tank that will be connected to a web server. The server will send json messages to certain topics on AWS where the tank (Raspberry Pi) will receive the messages and execute the commands.

## Software Used
* [NodeJs](https://nodejs.org/en/download)

## Libraries / Frameworks
* Front-End
    * [React](https://react.dev/)
    * [Vite](https://vitejs.dev/)
    * [Axios](https://axios-http.com/docs/intro)
* Back-end
    * [aws-iot-device-sdk](https://github.com/aws/aws-iot-device-sdk-js)
    * [Cors](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
    * [Express](http://expressjs.com/en/starter/installing.html)

## To Run / Test
* Get the [SDK](https://github.com/aws/aws-iot-device-sdk-python) onto the pi and have certificates ready from aws to run commands to the pi from the client
    * create folder in the `~` directory called `certs` and place all of your certification files in there.
    * You should put the `main.py` folder provided into the `samples/` folder in the repo and run the following:
        * `python3 pubsub.py --topic topic_1 --ca_file ~/certs/Amazon-root-CA-1.pem --cert ~/certs/certificate.pem.crt --key ~/certs/private.pem.key --endpoint <your aws endpoint here>`
        * now it should listen for commands from the tank client interface until it hears reverse.
* Pull client and server [code](https://github.com/kevinthedang/IoT-nerf-tank)
    * You will need to add your certifications into the `server` directory as a folder named `certifs`
    * You will also need a json file named `endpoint.json` to hold your endpoint for the server to connect to:
        * i.e. `{ "endpoint": "<your_endpoint_here>" }`
    * NodeJs must be install to run the client and sever
        * go into the `client` directory and run `npm i` then `npm start`
        * go into the `server` directory and run `npm i` then `npm start`
        * not the server should be up at `localhost:5173` most likely (or whatever vite tells you its hosted at)
    * Now you can click on the buttons and the Pi should receive the messages!


## Parts
* Refer to: 
    * `Parts_List.xlsx` in the `extras` folder for all the turret parts bought
    * [Bluetooth Nerf Turret - Hardware](https://www.littlefrenchkev.com/bluetooth-nerf-turret/#comp-k1tpv8jv)
    * [SZDoit Black T300 Tank Chassis](https://www.amazon.com/SZDoit-Raspberry-Learning-Caterpillar-Platform/dp/B08HRTZNHW/ref=sr_1_1?crid=G1VU0HSPKZJ4&keywords=tank+chassis+SZDoit+Black+T300+Robot+tracked+car+for+Arduino%2FRaspberry+pi&qid=1676065310&refinements=p_n_availability%3A2661601011&rnid=2661599011&s=toys-and-games&sprefix=tank+chassis+szdoit+black+t300+robot+tracked+car+for+arduino%2Fraspberry+p%2Ctoys-and-games%2C113&sr=1-1)
    * [Raspberry Pi](https://www.adafruit.com/product/4296)

## Credit
* [Kole Davis](https://github.com/Kole0518)
* [Drew Bogdan](https://github.com/DrewBogdan)
* [Vincent Do](https://github.com/VinnyVinVince)
* [Kevin Dang](https://github.com/kevinthedang)

## License
MIT License

Copyright (c) 2023 Kevin Dang, Drew Bogdan, Vincent Do, Kole Davis

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