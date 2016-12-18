apt-get install apache2
apt-get install nginx
a2enmod cgi
cp index.py /var/www/index.py
cp apache2-sysinfo.conf /etc/apache2/sites-available/apache2-sysinfo.conf
cp nginx-sysinfo.conf /etc/nginx/sites-enabled/nginx-sysinfo.conf
service nginx restart
a2ensite apache2-sysinfo
service apache2 reload
service apache2 restart
crontab cron.bak