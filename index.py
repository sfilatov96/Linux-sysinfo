#!/usr/bin/python
# -*- coding:utf-8 -*-

import cgi,cgitb
from datetime import datetime
import os
from  subprocess import check_output
from collections import Counter

cgitb.enable()
mpstat = []
iostat = []
mpstat_metrics = {}
mpstat = check_output("awk '{ print $3,$4,$5,$6,$12; }' /var/log/mpstat.log | tail -n 1 ",shell=True).replace("\n","").replace(",",".").split(" ")
iostat_titles = " r/s   w/s   await   util" 
iostat = check_output("awk '{ print $4,$5,$10,$14; }' /var/log/iostat.log | tail -n 1 ",shell=True).split("\n")
tcp_conn = check_output("awk '{ print $1,$2,$3,$4,$5; }' /var/log/tcp_conn.log",shell=True).split("\n")
udp_conn = check_output("awk '{ print $1,$2,$3,$4,$5; }' /var/log/udp_conn.log",shell=True).split("\n")
inodes = check_output("awk '{ print $1,$4,$5; }' /var/log/inodes.log",shell=True)[:-1].split("\n")
free_spaces = check_output("awk '{ print $1,$4,$5; }' /var/log/disk_spaces.log",shell=True)[:-1].split("\n")
tcp_stat = check_output("awk '{ print $1; }' /var/log/tcp_conn.log",shell=True)[:-1].split("\n")
network_loading=check_output("awk '{ print $1,$2,$3,$10,$11; }' /var/log/network_loading.log",shell=True)[:-1].split("\n")
nproc = int(check_output("nproc",shell=True))



if mpstat != ['']:

	mpstat = map(float,mpstat)
	mpstat_metrics['user(%)(us+ni)'] = mpstat[0]+mpstat[1]
	mpstat_metrics['sys(%)'] = mpstat[2]
	mpstat_metrics['iowait(%)'] = mpstat[3]
	mpstat_metrics['idle(%)'] = mpstat[4]


print "Content-Type: text/html; charset=utf-8"
print ""
print "<html><body>"

print "<b>NGINX_ADDR:</b>: %s</br>" % (os.environ['REMOTE_ADDR'])
print "<b>NGINX_PORT:</b>: %s</br>" % (os.environ['REMOTE_PORT'])
print "<b>CLIENT_ADDR:</b>: %s</br>" % (os.environ['HTTP_X_REAL_IP'])
print "<b>CLIENT_PORT:</b>: %s</br>" % (os.environ['HTTP_X_FORWARDER_FOR_PORT'])
print "<b>NGINX_VERSION:</b>: %s</br>" % (os.environ['HTTP_X_NGX_VERSION'])

if mpstat != ['']:
	print "<table border='1' width='1000'>"

	print "<tr><td>Load Average</td><td>"
	loadavg = os.getloadavg()
	for  i in loadavg:

		if i >= nproc :
			print "<p style='color:red'>%s</p>" % str(i)
		else:
			print "<p style='color:green'>%s</p>" % str(i)


	# if loadavg[0] < loadavg[1] < loadavg[2]:
	# 	print u'нагрузка падает'

	# if loadavg[0] > loadavg[1] > loadavg[2]:
	#  	print u'нагрузка растёт'


	print "</td></tr>"


	print "<tr><td>Load Disks</td><td>"
	print iostat_titles + "<br>"
	for i in iostat:
		print i + '<br>'
	print "</td></tr>"




	print "<tr><td>TCP<br>connections</td><td>"
	for param in tcp_conn:
		print "<p>%s</p>" % (param)
	print "</td></tr>"

	print "<tr><td>UDP<br>connections</td><td>"
	for param in udp_conn:
		print "<p>%s</p>" % (param)
	print "</td></tr>"


	print "<tr><td>TCP<br>connection status</td><td>"
	counts = Counter(tcp_stat)
	counts.pop("State")

	for key in counts:
		print"<p> %s -- %s </p>" % (key,counts[key])
	print "</td></tr>"







	print "<tr><td>CPU</td><td>"


	if mpstat:
		for param in mpstat_metrics:
			if mpstat_metrics[param] > 90:
				print "<p style='color:red'>%s  -- %s </p>" % (param,mpstat_metrics[param])
			elif 80 < mpstat_metrics[param] < 90:
				print "<p style='color:yellow'>%s  -- %s </p>" % (param,mpstat_metrics[param])
			else:
				print "<p style='color:green'>%s  -- %s </p>" % (param,mpstat_metrics[param])
		print "</td></tr>"


	print "<tr><td>Disk spaces</td><td>"
	print "<p>Файл.сис -- Свободно  -- Занято</p>"
	for i in free_spaces:
		d = i.split(" ")
		k = d[2]
		if k != '-':
			k = int(k[:-1])
			if d[0] not in ['/sys','/proc','/dev']:
				if k > 90:
					print "<p style='color:red'>%s  -- %s -- %s</p>" % (d[0],d[1],d[2])
				elif 80 < k < 90:
					print "<p style='color:yellow'>%s  -- %s -- %s</p>" % (d[0],d[1],d[2])
				else:
					print "<p style='color:green'>%s  -- %s -- %s</p>" % (d[0],d[1],d[2])
	print "</td></tr>"

	print "<tr><td>Inodes</td><td>"
	print "<p>Файл.сис -- Свободно  -- Занято</p>"
	for i in inodes:
		d = i.split(" ")
		k = d[2]
		if k != '-':
			k = int(k[:-1])
			if d[0] not in ['/sys','/proc','/dev']:
				if k > 90:
					print "<p style='color:red'>%s  -- %s -- %s</p>" % (d[0],d[1],d[2])
				elif 80 < k < 90:
					print "<p style='color:yellow'>%s  -- %s -- %s</p>" % (d[0],d[1],d[2])
				else:
					print "<p style='color:green'>%s  -- %s -- %s</p>" % (d[0],d[1],d[2])
	print "</td></tr>"


	print "<tr><td >Network Loading</td><td><table border='1'><tr><td></td><td colspan='2'>"
	print "Принято</td><td colspan='2'> Отправлено</td></tr>"
	print "<tr><td></td><td>байт</td><td>пакетов</td><td>байт</td><td>пакетов</td></tr>"
	for param in network_loading:
		param = param.split(' ')
		print "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (param[0],param[1],param[2],param[3],param[4])
	print "</table></td></tr>"

	print "</table>"
else:
	print "<h1>Данных пока нет, обновитесь(они появятся через минуту)</h1>"

print "</html></body>"








