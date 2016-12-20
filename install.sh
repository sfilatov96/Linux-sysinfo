apt-get update
apt-get -y install apache2
apt-get -y install nginx
apt-get -y install sysstat
apt-get install python-minimal
a2enmod cgi
cp index.py /var/www/html/index.py
chmod +x /var/www/html/index.py
cp apache2-sysinfo.conf /etc/apache2/sites-available/apache2-sysinfo.conf
rm /etc/nginx/sites-enabled/default
cp nginx-sysinfo.conf  /etc/nginx/sites-enabled/default
cat ports.conf > /etc/apache2/ports.conf 
a2ensite apache2-sysinfo
service apache2 reload
service apache2 restart
crontab cron.bak
service nginx restart
touch /var/log/mpstat.log  /var/log/iostat.log  /var/log/tcp_conn.log /var/log/udp_conn.log /var/log/inodes.log /var/log/disk_spaces.log /var/log/network_loading.log

