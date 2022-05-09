#!/bin/bash
echo "Starting server and sensors"
python server.py &
python sensor.py kitchen 1 &
python sensor.py bathroom 1 &
python sensor.py bedroom1 1 &
python sensor.py bedroom2 1 &
python sensor.py bedroom3 1 &
echo "All devices running"