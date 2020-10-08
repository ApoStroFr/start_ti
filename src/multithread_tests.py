from threading import Thread
import os

class Exec_test(Thread):
	""" Thread in charge of test several web-configuration"""

	def __init__(self, test, target):
		Thread.__init__(self)
		self.test = test
		self.target = target

	def run(self):
		if self.test == "testssl":
			self.exec_testssl()
		elif self.test == "dirb":
			self.exec_dirb()
		elif self.test == "nmap":
			self.scan_nmap()

	def exec_testssl(self):
		print("[+] sslcompare is starting it work.")
		os.system("bash sslcompare/testssl.sh/testssl.sh "+self.target.protocol+"://"+self.target.target_name+" > "+self.target.project_name+"/ssl_result/testssl_result 2> "+self.target.project_name+"/ssl_result/testssl_errors.log")
		print("[+] sslcompare has finished it works.")

	def exec_dirb(self):
		print("[+] dirbuster starts it work.")
		os.system("dirb "+self.target.protocol+"://"+self.target.target_name+" -o "+self.target.project_name+"/dirbuster_result/dirb_root_result -S > /dev/null 2> "+self.target.project_name+"/dirbuster_result/dirb_root_log")
		print("[+] dirbuster has finished it work.")

	def scan_nmap(self):
		print("[+] nmap is strating it work.")
		os.system("nmap -Pn -O -sV "+self.target.target_name+" >"+self.target.project_name+"/nmap_result/nmap_result")
		print("[+] nmap is strating it work.")