# Simple install/remove makefile
#

install:
	cp RobotJoxLightServer.py /usr/local/bin/
	cp RobotJoxLightServer.service /usr/lib/systemd/system/

uninstall:
	rm -f /usr/local/bin/RobotJoxLightServer.py
	rm -f /usr/lib/systemd/system/RobotJoxLightServer.service

service-enable:
	systemctl daemon-reload
	systemctl enable RobotJoxLightServer

service-start:
	service RobotJoxLightServer start

service-stop:
	service RobotJoxLightServer stop

install-deps:
	pip3 install -r requirements.txt
