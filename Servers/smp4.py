import httplib, urllib2, pickle
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


sources = { "SCART": 65,
		  	"TV": 0, 
		  	"HDMI1": 57, 
		  	"HDMI2": 58, 
		  	"HDMI3": 59, 
		  	"HDMI4": 60, 
		  	"AV": 28, 
		  	"COMPONENT": 41
		   }

class TVControl:


	def __init__(self,hostname):
		self.Hostname=hostname

	def SendSOAP(self,method,body):
		print '*',method

		headers = {
			"Content-type": 'text/xml;charset="utf-8"', 
			"SOAPACTION": '"urn:samsung.com:service:MainTVAgent2:1#%s"' % method
		}

		conn = httplib.HTTPConnection(self.Hostname)
		conn.request("POST", "/smp_4_", body, headers)

		response = conn.getresponse()
		print(response.status, response.reason)


		with open('dump.xml', 'w'): pass

		data = (response.read())
		file = open('dump.xml', 'w')
		file.write(data)
		file.close()
		out = ''
		for event, elem in ET.iterparse(dump.xml):
			if event == 'end':
				if elem.tag == 'Result':
					out = elem.txt 
			elem.clear()



		print('result ',out)
		print data
		#print ''
		#print data[data.index('<CurrentExternalSource>'):data.index('</CurrentExternalSource')]


		return data

	def GetSourceList(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:GetSourceList xmlns:u="urn:samsung.com:service:MainTVAgent2:1"></u:GetSourceList>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('GetSourceList',body)

	def GetCurrentExternalSource(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:GetCurrentExternalSource xmlns:u="urn:samsung.com:service:MainTVAgent2:1"></u:GetCurrentExternalSource>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('GetCurrentExternalSource',body)

	def SendMBRIRKey(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:SendMBRIRKey xmlns:u="urn:samsung.com:service:MainTVAgent2:1">'+\
						'<MBRDevice>STB</MBRDevice>'+\
						'<MBRIRKey>0x01</MBRIRKey>'+\
						'<ActivityIndex>0</ActivityIndex>'+\
					'</u:SendMBRIRKey>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('SendMBRIRKey',body)

	def SetMainTvSource(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:SetMainTVSource xmlns:u="urn:samsung.com:service:MainTVAgent2:1">'+\
						'<Source>%s</Source>' % source+\
						'<ID>%s</ID>'% id1+\
						'<UiID>0</UiID>'+\
					'</u:SetMainTVSource>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('SetMainTVSource',body)

	def StartCloneView(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
			'<s:Body>'+\
				'<u:StartCloneView xmlns:u="urn:samsung.com:service:MainTVAgent2:1">'+\
					'<ForcedFlag>Normal</ForcedFlag>'+\
					'<DRMType>PrivateTZ</DRMType>'+\
				'</u:StartCloneView>'+\
			'</s:Body></s:Envelope>'
		self.SendSOAP('StartCloneView',body)


if __name__ == '__main__':
	global source, id1
	print ("Your choice of Sources:")
	print ("SCART\nTV\nHMDI1\nHDMI2\nHDMI3\nHDMI4\nAV\nCOMPONENT")
	print ("Which would you like to use?")
	source = raw_input()
	id1 = sources[source]	
		
	tvcontrol=TVControl("192.168.0.181:7676")

	tvcontrol.SetMainTvSource()
	tvcontrol.GetCurrentExternalSource()
	#tvcontrol.GetSourceList()