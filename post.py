from sense_hat import SenseHat
from gpiozero import CPUTemperature
import time
import os
import requests


sense = SenseHat()
start_time = time.time() 

cpu = CPUTemperature()

host_name = os.uname()[1]
post_adress = "http://192.168.1.37:8080"
 
temp_r ="""<omiEnvelope xmlns="http://www.opengroup.org/xsd/omi/1.0/" version="1.0" ttl="0">
 <write msgformat="odf">
   <msg>
     <Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/">
       <Object>
         <id>"""+host_name+"""</id>
         <InfoItem name="temperature">
           <value>%s</value>
         </InfoItem>
       </Object>
     </Objects>
   </msg>
 </write>
</omiEnvelope>"""

cpu_temp_r ="""<omiEnvelope xmlns="http://www.opengroup.org/xsd/omi/1.0/" version="1.0" ttl="0">
 <write msgformat="odf">
   <msg>
     <Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/">
       <Object>
         <id>"""+host_name+"""</id>
         <InfoItem name="CPU_temperature">
           <value>%s</value>
         </InfoItem>
       </Object>
     </Objects>
   </msg>
 </write>
</omiEnvelope>"""



humid_r ="""<omiEnvelope xmlns="http://www.opengroup.org/xsd/omi/1.0/" version="1.0" ttl="0">
 <write msgformat="odf">
   <msg>
     <Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/">
       <Object>
         <id>"""+host_name+"""</id>
         <InfoItem name="humidity">
           <value>%s</value>
         </InfoItem>
       </Object>
     </Objects>
   </msg>
 </write>
</omiEnvelope>"""





while True:
	time.sleep(1)
	if time.time()- start_time > 1:
		
		sense = SenseHat()
		humidity = sense.get_humidity()
		print("Humidity: %.3f %%rH" % humidity)
		requests.post(post_adress, humid_r % humidity)

		time.sleep(2)
		temp = sense.get_temperature()
		print("Temperature: %.3f C" % temp)
		requests.post(post_adress, temp_r % temp)

		cpu_temp = cpu.temperature
		print("CPU-Temperature: %.3f C" % cpu_temp)
		requests.post(post_adress, cpu_temp_r % cpu_temp)
		start_time = time.time()


