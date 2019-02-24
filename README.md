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

`docker run -e SOCKET_HOST=piaware -e SOCKET_PORT="30003" -e MQTT_HOST="mqtt.example.com" -e MQTT_PORT="88883" -e MQTT_TOPIC="ADSB/adsb" -e MQTT_CLIENT_ID="adsb-consumer" -e MQTT_TLS="True"  socket-mqtt`


#### Sample Kubernetes Manifests

Config 

```bash
apiVersion: v1
kind: ConfigMap
metadata:
  name: adsb-to-mqtt
  namespace: default
data:
  SOCKET_HOST: "dump1090"
  SOCKET_PORT: "30003"
  MQTT_HOST: "mqtt.example.com"
  MQTT_PORT: "8883"
  MQTT_TOPIC: "ADSB/adsb"
  MQTT_CLIENT_ID: "adsb-to-mqtt"
  MQTT_TLS: "True"
  LOG_LEVEL: "INFO"

```

Deployment

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: adsb-to-mqtt
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: adsb-to-mqtt
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: adsb-to-mqtt
    spec:
      containers:
      - name: adsb-to-mqtt
        image: zebpalmer/socket-mqtt:latest
        imagePullPolicy: Always
        envFrom:
          - configMapRef:
              name: adsb-to-mqtt
      restartPolicy: Always


```