apt-get update
apt-get install apache2
apt-get install nginx
apt-get install sysstat
a2enmod cgi
cp index.py /var/www/index.py
cp index.py /var/www/html/index.py
chmod 777 /var/www/index.py
chmod 777 /var/www/html/index.py
cp apache2-sysinfo.conf /etc/apache2/sites-available/apache2-sysinfo.conf
rm /etc/nginx/sites-enabled/default
cp nginx-sysinfo.conf > /etc/nginx/sites-enabled/default
cat ports.conf > /etc/apache2/ports.conf 
service nginx restart
a2ensite apache2-sysinfo
service apache2 reload
service apache2 restart
crontab cron.bak
chmod 777 /var/log/tcpdump.log