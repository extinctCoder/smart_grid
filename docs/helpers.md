## 🔐 Creating an MQTT Password File Using Docker

To secure your Mosquitto MQTT broker with user authentication, you need a password file containing encrypted credentials. This section explains how to create that password file using a temporary Docker container running `mosquitto_passwd`.

### 🛠️ Command

```bash
# Create a password file for the MQTT broker user 'extinctcoder'
# This uses a temporary Docker container to run mosquitto_passwd

# It mounts the local directory 'docker/mosquitto/config' into the container
# The password file will be created at: docker/mosquitto/config/password.txt

docker run -it --rm \
  -v "$PWD/docker/mosquitto/config:/mosquitto/config" \
  eclipse-mosquitto \
  mosquitto_passwd -c /mosquitto/config/password.txt extinctcoder
```
