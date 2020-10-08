import re

class Switcher_h(object):

	def __init__(self, headers_tested):
		self.not_bp_header = {"X-Frame-Options":"Header missing", "X-XSS-Protection":"Header missing", "Date":"Header missing", "X-Content-Type-Options":"Header missing", "Content-Type":"Header missing", "Strict-Transport-Security":"Header missing", "Content-Security-Policy":"Header missing", "Cache-Control":"Header missing"}
		self.headers_tested = headers_tested

	def switch(self, header):
		method_name='case_'+re.sub("\-+", "_", header).lower()
		try:
			return getattr(self,method_name,lambda:"")(header)
		except TypeError:
			pass;

	#Test le content de X-FRAME-OPTIONS
	def case_x_frame_options(self, header):
		if self.headers_tested[header].lower() == "deny" or self.headers_tested[header].lower() == "sameorigin":
			self.not_bp_header.pop("X-Frame-Options")
		else:
			self.not_bp_header["X-Frame-Options"] = "Bad implemenation, wrong value used"

	#Test le content de X-XSS-PROTECTION
	def case_x_xss_protection(self,header):
		if self.headers_tested[header] == "1" or self.headers_tested[header] == "1; mode=block":
			self.not_bp_header.pop('X-XSS-Protection')
		else:
			self.not_bp_header["X-XSS-Protection"]="Bad implementation, wrong value used"


	#Test le content de X-CONTENT-TYPE-OPTIONS
	def case_x_content_type_options(self,header):
		self.not_bp_header.pop("X-Content-Type-Options")


	#Test le content de STRICT-TRANSPORT-SECURITY
	def case_strict_transport_security(self,header):
		self.not_bp_header.pop("Strict-Transport-Security")

	#Test le content de STRICT-TRANSPORT-POLICY
	def case_content_security_policy(self,header):
		self.not_bp_header.pop("Content-Security-Policy")

	#Test le content de CACHE-CONTROL
	def case_cache_control(self,header):
		self.not_bp_header.pop("Cache-Control")

	#Test le content de SERVER
	def case_server(self,header):
		self.not_bp_header["Server"] = "Information Leak"
	
	#Test le content de X-POWERED-BY
	def case_content_type(self,header):
		self.not_bp_header.pop("Content-Type")

	def case_x_powered_by(self,header):
		self.not_bp_header["X-Powered-By"] = "Information leak"

	def case_date(self, header):
		self.not_bp_header.pop("Date")

	def get_result(self):
		return self.not_bp_header