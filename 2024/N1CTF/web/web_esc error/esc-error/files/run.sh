gcc -o /readflag /readflag.c && \
rm /readflag.c && \
echo $FLAG > /flag && \
chmod 400 /flag && \
unset FLAG && \
chmod u+s /readflag

su ctf -c 'mysqld &' && \
sleep 5 && \
mysql -e "CREATE DATABASE IF NOT EXISTS mydb;" && \
mysql -e "CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';" && \
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost';" && \
mysql -e "FLUSH PRIVILEGES;" && \
mysql -e "CREATE TABLE mydb.user (username VARCHAR(50) PRIMARY KEY, email VARCHAR(100) NOT NULL);"

su ctf -c 'supervisord'