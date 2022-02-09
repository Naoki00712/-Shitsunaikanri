# Oct 20th 2021 N.Matsumoto
#
# sudo apt install i2c-tools
# git clone https://github.com/adafruit/Adafruit_Python_BMP.git
# cd Adafruit_Python_BMP
# sudo python3 setup.py install

import Adafruit_BMP.BMP085 as BMP085
import ambient
import dht11
import RPi.GPIO as GPIO
import requests,json
import statistics
import time

sensor = BMP085.BMP085()

DHT = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DHT, GPIO.IN)

OW = requests.get('https://api.openweathermap.org/data/2.5/weather?units=metric&q=Kobe,jp&appid=c6ccc4bf18551176bc9fe1ac4cc83e0f').json()

OWS = str(OW)

CHANNELID = '42764'
WRITEKEY = '815e16cd06c95de3'

am = ambient.Ambient(CHANNELID, WRITEKEY)

sensor2 = dht11.DHT11(pin=DHT)

temperature = []
humidity = []

for i in range(4):
    while True:
        result = sensor2.read()

        if result.is_valid() == False:
            print("error date")
            time.sleep(3)
            continue

        break
    temperature.append(result.temperature)
    humidity.append(result.humidity)

    dt = time.strftime("%Y-%m-%d %H:%M:%S")
    date = { 'created': dt, 'd1': result.temperature, 'd2': result.humidity,}
    print("number  :",i,date)
    
    time.sleep(3)


temperature_ave = round(statistics.mean(temperature),2)
humidity_ave = round(statistics.mean(humidity),2)

dt = time.strftime("%Y-%m-%d %H:%M:%S")
date = { 'created': dt, 'd1': temperature_ave, 'd2': humidity_ave,}
print("average : 4",date)

time.sleep(3)

#print(OWS)

#print(str(OW["main"]["temp_min"]))

while True:
    temp = sensor.read_temperature()
    pres = sensor.read_pressure() /100
    alti = sensor.read_altitude(sealevel_pa=102000)
    
    # 現在日時を取得
    dt = time.strftime("%Y-%m-%d %H:%M:%S")

    date = { 'created': dt, 'd1': temperature_ave, 'd2': humidity_ave, 'd3': pres,}
    print("BMPpres : 5",date)
    
    time.sleep(3)
    
    #print('温度: {0:0.2f} °C,気圧: {1:0.2f}, hPa標高: {2:0.2f} m'.format(temp, pres, alti))
    #print('気圧 = {0:0.2f} hPa'.format(pres))
    #print('標高 = {0:0.2f} m\n'.format(alti))
    
    # チャンネルに日時情報と一緒にメッセージを送る
    #message = now + "神戸市の温度 : " + str(OW["main"]["temp"]) + " °C  湿度 : " + str(OW["main"]["humidity"]) + "% \n"
    #print(message)

    dt = time.strftime("%Y-%m-%d %H:%M:%S")
    date = { 'created': dt, 'd1': temperature_ave, 'd2': humidity_ave, 'd3': pres, 'd4': OW["main"]["temp"], 'd5': OW["main"]["humidity"], 'd6': OW["main"]["pressure"],} 
    print("kobe +  : 6",date)
    
    time.sleep(3)
    
    response = am.send(date)
    
     break
