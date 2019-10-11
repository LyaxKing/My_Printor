# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:57:51 2019

@author: HP
"""
import aliyunsdkiotclient.AliyunIotMqttClient as iot
import time


class MqttClient:
    def __init__(self, options, host):
        self.host = host
        self.options = options
        self.client = iot.getAliyunIotMqttClient(options['productKey'], options['deviceName'], options['deviceSecret'],
                                              secure_mode=3)

    def on_subscribe(client, userdata, mid, granted_qos):
        print("On Subscribed: qos = %d" % granted_qos)

    def on_message(self,client, userdata, msg):
        self.check_file = msg.payload
        print(msg.payload)

    def on_connect(self,client, userdata, flags_dict, rc):
        print("Connected with result code " + str(rc))

    def on_disconnect(self,client, userdata, flags_dict, rc):
        print("Disconnected.")
        topic_gcode = '/sys/' + self.options['productKey'] + '/' + self.options['deviceName'] + '/user/gcode'
        self.client.subscribe(topic_gcode)

    def pubilish_status(self, statue_json):
        topic = '/sys/' + self.options['productKey'] + '/' + self.options['deviceName'] + '/thing/event/property/post'
        topic_sever = '/sys/' + self.options['productKey'] + '/' + self.options['deviceName'] + '/user/statue'
        payload_json = {
            'id': int(time.time()),
            'params': statue_json,
        'method': "thing.event.property.post"
        }
        print('send data to iot server: ' + str(payload_json))
        self.client.publish(topic, payload=str(payload_json))
        self.client.publish(topic_sever, payload=str(payload_json))

    def start_client(self):
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.connect(host=self.host, port=self.options['port'], keepalive=60)
        self.client.loop_forever()



