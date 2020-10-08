#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from src import project,target


protocole="https"
ssl=True
dirb=True
nmap=True
compteur = 0
for i in sys.argv:
	compteur+=1
	print(i)
	if i == "-p" or i == "--project":
		path = sys.argv[compteur]
	if 	i == "-u" or i == "--url":
		url = sys.argv[compteur]
	if i == "-P" or i == "--Protocol":
		protocole = sys.argv[compteur]
		if not protocole == "http" or protocole == "https":
			print("error argument")
			exit()
	if i == "--no-ssl":
		ssl=False
	if i == "--no-dirb":
		dirb=False
	if i == "--no-nmap":
		nmap=False

project.create(path)
mytarget=target.Target(url,path,protocole,ssl,dirb,nmap)
mytarget.get_all()