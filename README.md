# IoT
開啟伺服器：uvicorn main:app --port 9000 --reload
mqtt 測試發送指令：mosquitto_pub -h broker.emqx.io -p 1883 -t /python/mqtt/hst/dht22 -m "29.4"
mqtt 測試接收指令：mosquitto_sub -h broker.emqx.io -p 1883 -t /python/mqtt/hst/cmd/+