compile
arduino-cli compile --fqbn arduino:avr:uno blink/

flash
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno blink/
