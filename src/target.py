#!/usr/bin/env python
import sys
import dns.resolver #pip install dnspython
import json
import requests
import os
from src import best_practices as bp
from src import multithread_tests as mt
from pywhatcms import whatcms
import subprocess


#Définition de la classe Target:
class Target(object):
	"""Classe définissant le site web cible. Il est caractérisé par:
		- Son noms au format URL
		- Son/ses adresses IPs
		- Méthodes HTTPs possibles
		- CMS utilisé
		- Headers utilisés
		- Project name
	"""
	#Constructeur
	def __init__(self, target_name, project_name, protocol,ssl,dirb,nmap):

		whatcms_key='5355e8946fa80836c2c3d11cdfcd4ce52aeef5490c48c8ca11bbce15a6634fc413bacc'
		self.project_name = project_name
		self.target_name = target_name
		self.protocol = protocol
		self.ssl = ssl
		self.dirb = dirb
		self.nmap = nmap

		if self.ssl:
			#Initialisation et execution du multi.thread pour gagner du temps
			mt_testssl = mt.Exec_test("testssl", self)
			mt_testssl.start()


		if self.dirb:
			#Initialisation et execition du multithread pour gagner du temps
			mt_dirb = mt.Exec_test("dirb", self)
			mt_dirb.start()


		if self.nmap:
			mt_nmap = mt.Exec_test("nmap", self)
			mt_nmap.start()
		

		
		self.ip = {}


		#Requète DNS pour trouver les @IPs
		try:
			answers_ipv4 = dns.resolver.query(self.target_name, 'A')
			compteur = 0
			for rdata in answers_ipv4:
				compteur += 1
				self.ip[compteur]= rdata.address
		except dns.resolver.NoAnswer:
			print("*** No AAA record for "+host+" ***")
		except dns.resolver.NXDOMAIN:
			print("*** The name"+host+" does not exist ***")

		
		#Requêtes pour connaitre les Headers utilisés
		#selon les headers
		req_get = requests.get(self.protocol+"://"+self.target_name)
		self.headers_used = dict(req_get.headers)

		#Création d'un switcher qui vas tester les bonnes pratiques des Headers
		s = bp.Switcher_h(self.headers_used)
		
		#Pour chaque header du site, je teste si il utilisent les bonnes pratiques
		for header in self.headers_used:
			s.switch(header)

		#J'écris le résultat dans un nouvel attribut
		self.headers_security_test = s.get_result()



		#Requète utilisant whatcms.org : utiliser sa propre API
		whatcms_key='5355e8946fa80836c2c3d11cdfcd4ce52aeef5490c48c8ca11bbce15a6634fc413bacc'
		whatcms = requests.get('https://whatcms.org/APIEndpoint/Detect?key='+whatcms_key+'&url='+self.target_name).json()
		whatcms.pop("request")
		whatcms.pop("private")
		self.cms_used = whatcms

		### PARTIE A REVOIR
		#req_opt = requests.options("https://"+self.target_name)
		req_opt = requests.request('OPT',self.protocol+"://"+self.target_name)
		if req_opt.status_code == 200:
			try:
				self.methodHTTP_allowed = req_opt.headers['Allow']

			except:
				self.methodHTTP_allowed = 'OPT accepted, but no more information'

			else :
				self.methodHTTP_allowed = 'OPTIONS accepted, no information'
		else:
			with open('db/HTTP_statuscode.json') as json_file:
				HTTPsc = json.load(json_file)
				status_code_str = str(req_opt.status_code)
				self.methodHTTP_allowed = status_code_str+' - '+HTTPsc[status_code_str]["title"]
		### FIN DE PARTI A REVOIR

		#self.metthodHTTP_allowed = A AMELIORER
		#Créer un module qui indique quel type d'erreur corespond à quoi avec une fonction get_titel etc...


		#Exécute testssl > testssl_result	
		os.system("python sslcompare/sslcompare.py -u "+protocol+"//"+self.target_name+" > "+self.project_name+"/ssl_result/sslcompare_result 2> "+self.project_name+"/ssl_result/sslcompare_errors.log")
		#Multi-thread here
		#nmap

		if self.ssl:
			#Fin du multithread de testssl :
			mt_testssl.join()

		if self.dirb:	
			# Fin du multithread de Dirbuster :
			mt_dirb.join()

		if self.nmap:
			mt_nmap.join()
		

	
	def get_all(self):
		formated_json = json.dumps(self.__dict__, indent=4)
		#formated_json.pop(dirb,ssl)
		print(formated_json)