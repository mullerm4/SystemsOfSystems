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
         <InfoItem name="humidity">
           <value>%s</value>
         </InfoItem>
         <InfoItem name="temperature">
           <value>%s</value>
         </InfoItem>
         <InfoItem name="CPU_Temperature">
           <value>%s</value>
         </InfoItem>
         <InfoItem name="Temperature_Diff">
           <value>%s</value>
         </InfoItem>
         <InfoItem name="CPU_usage">
           <value>%s</value>
         </InfoItem>
         <InfoItem name="Memory_usage">
           <value>%s</value>
         </InfoItem>
       </Object>
     </Objects>
   </msg>
 </write>
</omiEnvelope>"""



sense = SenseHat()

while True:

	time.sleep(3)

	humidity = sense.get_humidity()
	print("Humidity: %.3f %%rH" % humidity)

	temp = sense.get_temperature()
	print("Temperature: %.3f C" % temp)


	cpu_temp = cpu.temperature
	print("CPU-Temperature: %.3f C" % cpu_temp)

	temp_diff = cpu_temp - temp
	print("Temperature difference %.3f C" % temp_diff)

	cpu_usage = psutil.cpu_percent()
	print("CPU-usage: %.3f %%" % cpu_usage)



	memory_usage = psutil.virtual_memory()[2]
	print("RAM-usage: %.3f %%" % memory_usage)



	requests.post(post_adress, request_r % (humidity, temp, cpu_temp, cpu_usage, memory_usage))


