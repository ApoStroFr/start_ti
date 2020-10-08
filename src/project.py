#!/usr/bin/env python
import os

def create(path):

	if not os.path.exists(path):
		os.mkdir(path)
		print('Projet directory created at'+path)
	else:
		print('Project already created ! \nPick another project name.')
	if not os.path.exists(path+'/nmap_result'):
		os.mkdir(path+'/nmap_result')
	if not os.path.exists(path+'/dirbuster_result'):
		os.mkdir(path+'/dirbuster_result')
	if not os.path.exists(path+'/ssl_result'):
		os.mkdir(path+'/ssl_result')
