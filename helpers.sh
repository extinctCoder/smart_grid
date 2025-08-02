# Create a password file for the MQTT broker user 'extinctcoder'
# This runs mosquitto_passwd in a Docker container to generate an encrypted password
# The password file will be created at docker/mosquitto/config/password.txt
docker run -it --rm -v "$PWD/docker/mosquitto/config:/mosquitto/config" eclipse-mosquitto mosquitto_passwd -c /mosquitto/config/password.txt extinctcoder
