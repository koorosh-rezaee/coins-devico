export MYIP=`ifconfig | grep -A 1 eth0 | grep inet | cut -f 2 -d "t" | cut -f 2 -d " "`

sudo INT=$MYIP docker compose down -v

