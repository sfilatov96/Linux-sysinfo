apt-get install apache2
apt-get install nginx
a2enmode cgi
cp index.py /var/www/index.py
cp apache-sysinfo.conf /etc/apache2/sites-enabled/apache-sysinfo.conf
cp nginx-sysinfo.conf /etc/nginx/sites-availible/nginx-sysinfo.conf
service nginx restart
a2ensite apache-sysinfo
service apache2 reload
service apache2 restart
crontab cron.bak