from microDNSServer import MicroDNSSrv
from randomnick import generar_nick
import network
from time import sleep
from machine import Pin, PWM
from microdot import Microdot, send_file, redirect
from microdot.websocket import with_websocket
import math
import esp
esp.osdebug(None)
import gc
gc.collect()
try:
    f = open("ap.txt", "r")
    ap_name=f.read()
    if ap_name == '':
      f = open("ap.txt", "w")
      f.write(generar_nick())
      f.close()
      f = open("ap.txt", "r")
      ap_name=f.read()
    f.close()
except:
    f = open("ap.txt", "w")
    f.write(generar_nick())
    f.close()
    f = open("ap.txt", "r")
    ap_name=f.read()
    f.close()
ssid = ap_name
f.close()
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=str(ssid), authmode=network.AUTH_OPEN)

while ap.active() == False:
  pass

MicroDNSSrv.Create({ '*' : str(ap.ifconfig()[0]) })
app = Microdot()
pinMotorIzq = [ PWM(Pin(0, Pin.OUT), freq=20000), PWM(Pin(1, Pin.OUT), freq=20000)]
pinMotorDer = [ PWM(Pin(2, Pin.OUT), freq=20000), PWM(Pin(3, Pin.OUT), freq=20000)]
pi=3.141592
perim = 6.7*pi
r=133 #distancia entre ruedas  |<--- r --->|

def Duty(mot: list, duty: int):
    print("DUTY"+str(duty))
    duty=int(duty)
    if duty > 1023:
        print(duty)
        duty = 1023
    elif duty < -1023:
        print(duty)
        duty = 0
    if duty > 0:
        mot[0].duty(duty)
    elif duty < 0:
        mot[1].duty(-duty)
    elif duty == 0:
        mot[0].duty(0)
        mot[1].duty(0)
def giro(x: int, y: int):
    if x > 100:
        x=100
    elif x < -100:
        x=-100
    if y > 100:
        y=100
    elif y < -100:
        y=-100
    if x >= 0:
        Duty(pinMotorIzq,10.23*y)
        Duty(pinMotorDer,10.23*y*(100-x)/100)
    else:
        Duty(pinMotorIzq,10.23*y*(x+100)/100)
        Duty(pinMotorDer,10.23*y)
     
@app.route('/')
async def index(request):
    return send_file('index.html')

@app.route('/giro')
@with_websocket
async def echo(request, ws):
    while True:
        data = await ws.receive()
        print(data)
        giro(*[int(x) for x in data.split(",")])
        
@app.errorhandler(404)
async def not_found(request):
    return redirect('/')

app.run(port=80)
