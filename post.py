from sense_hat import SenseHat
from gpiozero import CPUTemperature
import time
import os
import requests
import psutil


sense = SenseHat()
start_time = time.time() 

cpu = CPUTemperature()

host_name = os.uname()[1]
post_adress = "http://192.168.1.37:8080"
 



request_r ="""<omiEnvelope xmlns="http://www.opengroup.org/xsd/omi/1.0/" version="1.0" ttl="0">
 <write msgformat="odf">
   <msg>
     <Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/">
       <Object>
         <id>"""+host_name+"""</id>
         <InfoItem name="sensors">
           <humidity>%s</humidity>
           <temperature>%s</temperature>
           <cpu_temperature>%s</cpu_temperature>
         </InfoItem>
         <InfoItem name="res_utilization">
           <cpu_usage>%s</cpu_usage>
           <memory_usage>%s</memory_usage>
         </InfoItem>
       </Object>
     </Objects>
   </msg>
 </write>
</omiEnvelope>"""



sense = SenseHat()

while True:
	time.sleep(1)
	if time.time()- start_time > 1:
		

		humidity = sense.get_humidity()
		print("Humidity: %.3f %%rH" % humidity)


		time.sleep(2)
		temp = sense.get_temperature()
		print("Temperature: %.3f C" % temp)


		cpu_temp = cpu.temperature
		print("CPU-Temperature: %.3f C" % cpu_temp)

		cpu_usage = psutil.cpu_percent()
		print("CPU-usage: %.3f %%" % cpu_usage)

		memory_usage = psutil.virtual_memory()[2]
		print("RAM-usage: %.3f %%" % memory_usage)

		requests.post(post_adress, request_r % (humidity, temp, cpu_temp, cpu_usage, memory_usage))
		start_time = time.time()

