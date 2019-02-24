# Socket to MQTT
*Dockerized script to grab every line output on a socket and throw the line onto MQTT topic.*

#### Why
I needed an app that I could deploy to kubernetes that would read lines from a socket and output 
 those lines to a MQTT broker. In my use initial use case, I needed raw ADS-B data from dump1090
 to be thrown onto a remote MQTT broker. This does that. Noting more. 

**Note:** There is very little or no error handling in this script. In most error cases, I'd rather
 the container die and let docker/swarm/kubernetes create a new instance. 

## Config
As the main deploy scenario for this script is via docker (Docker Compose, Docker Swarm, 
Kubernetes) all configuration is done via environment variables. 


##### Required
* SOCKET_HOST
* SOCKET_PORT
* MQTT_HOST
* MQTT_PORT
* MQTT_TOPIC 


##### Optional
* MQTT_CLIENT_ID (default: random uuid)
* MQTT_TLS (default: False) Setting True will verify ssl cert
* LOG_LEVEL (default: 'INFO')

#### Sample Run Command

```bash 
docker run /
  --env SOCKET_HOST=piaware /
  --env SOCKET_PORT=30003 /
  --env MQTT_HOST=mqtt.example.com /
  --env MQTT_PORT=88883 /
  --env MQTT_TOPIC=ADSB/adsb /
  --env MQTT_CLIENT_ID=adsb-consumer /
  --env MQTT_TLS=True /
  socket-mqtt:latest



```
