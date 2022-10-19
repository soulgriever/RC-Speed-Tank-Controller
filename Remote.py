import usys
import ustruct as struct
import utime
from machine import Pin, SPI, ADC
from nrf24l01 import NRF24L01
from micropython import const

cfg = {"spi": 0, "miso": 4, "mosi": 7, "sck": 6, "csn": 14, "ce": 17}

#Joysticks
LJP = 27
RJP = 26
LJoy = ADC(Pin(LJP))
RJoy = ADC(Pin(RJP))
#Buttons
GDown = Pin(22,Pin.IN, Pin.PULL_UP)
GUp = Pin(21,Pin.IN, Pin.PULL_UP)
#Initial variables
Gear = 0
LS = 127
RS = 127

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
nrf = NRF24L01(SPI(cfg["spi"]), csn, ce)

nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])

while True:
    # stop listening and send packet
    #ADC reads in 12bits but then scales to 16bits then down to 8bits
    LS = LJoy.read_u16() >> 8
    RS = RJoy.read_u16() >> 8
    if GDown.value() == 0 or GUp.value() == 0:
        if GDown.value() == 0:
            if Gear > 0:
                Gear -= 1
                utime.sleep_ms(150)
        elif GUp.value() == 0:
            if Gear < 2:
                Gear += 1
                utime.sleep_ms(150)
    try:
        nrf.send(struct.pack("iii", LS, RS, Gear))
    except OSError:
        pass
    print(LS, RS, Gear)
