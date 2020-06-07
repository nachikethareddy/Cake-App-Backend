#!/bin/bash
sudo apt-get update -y
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl -y
sudo -H pip3 install --upgrade pip
sudo nginx -t && sudo systemctl restart nginx
sudo bash
sudo su
cd /home/ubuntu
git clone https://github.com/raysandeep/Cake-App-Backend
cd Cake-App-Backend/
sudo apt install virtualenv -y
virtualenv venv -p python3 && source venv/bin/activate
sudo chown -R ubuntu:ubuntu /home/ubuntu/Cake-App-Backend/venv
pip3 install -r requirements.txt
touch .env
echo "DEBUG = True" > .env
echo "SECRET_KEY = '44uyt0)4%y^nxq1buxi4xch0u-r4^*w*pmh4)fxnvqgw&y5t)k'" >> .env
sudo ufw allow 8000
deactivate
echo "Entering Gunicorn Socket"
sudo touch /etc/systemd/system/gunicorn.socket
sudo echo "[Unit]" > /etc/systemd/system/gunicorn.socket
sudo echo "Description=gunicorn socket" >> /etc/systemd/system/gunicorn.socket
sudo echo "" >> /etc/systemd/system/gunicorn.socket
sudo echo "[Socket]" >> /etc/systemd/system/gunicorn.socket
sudo echo "ListenStream=/run/gunicorn.sock" >> /etc/systemd/system/gunicorn.socket
sudo echo "" >> /etc/systemd/system/gunicorn.socket
sudo echo "[Install]" >> /etc/systemd/system/gunicorn.socket
sudo echo "WantedBy=sockets.target" >> /etc/systemd/system/gunicorn.socket
echo "Gunicorn Socket Done "
echo "Entering Gunicorn Service"
sudo touch /etc/systemd/system/gunicorn.service
sudo echo "[Unit]" > /etc/systemd/system/gunicorn.service
sudo echo "Description=gunicorn daemon" >> /etc/systemd/system/gunicorn.service
echo "Requires=gunicorn.socket" >> /etc/systemd/system/gunicorn.service
echo "After=network.target" >> /etc/systemd/system/gunicorn.service
echo "" >> /etc/systemd/system/gunicorn.service
echo "[Service]" >> /etc/systemd/system/gunicorn.service
echo "User=ubuntu" >> /etc/systemd/system/gunicorn.service
echo "Group=www-data" >> /etc/systemd/system/gunicorn.service
echo "WorkingDirectory=/home/ubuntu/Cake-App-Backend" >> /etc/systemd/system/gunicorn.service
echo "ExecStart=/home/ubuntu/Cake-App-Backend/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock backend.wsgi:application" >> /etc/systemd/system/gunicorn.service
echo "" >> /etc/systemd/system/gunicorn.service
echo "[Install]" >> /etc/systemd/system/gunicorn.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/gunicorn.service
echo "Gunicorn Service Done "
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn
curl --unix-socket /run/gunicorn.sock localhost
sudo systemctl status gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
echo "Gunicorn Check Done"

sudo touch /etc/nginx/sites-available/
echo "server {" > /etc/nginx/sites-available/backend
echo "    listen 80;" >> /etc/nginx/sites-available/backend
echo "    location = /favicon.ico { access_log off; log_not_found off; }" >> /etc/nginx/sites-available/backend
sudo echo "    location /static/ {" >> /etc/nginx/sites-available/backend
sudo echo "        root /home/ubuntu/Cake-App-Backend;" >> /etc/nginx/sites-available/backend
sudo echo "    }" >> /etc/nginx/sites-available/backend
sudo echo "" >> /etc/nginx/sites-available/backend
sudo echo "    location / {" >> /etc/nginx/sites-available/backend
sudo echo "        include proxy_params;" >> /etc/nginx/sites-available/backend
sudo echo "        proxy_pass http://unix:/run/gunicorn.sock;" >> /etc/nginx/sites-available/backend
sudo echo "    }" >> /etc/nginx/sites-available/backend
sudo echo "}" >> /etc/nginx/sites-available/backend
sudo echo "NGINX intial config done!"
sudo ln -s /etc/nginx/sites-available/backend /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
echo "Done -- Wozzby Deployed Succesfully!"