export MYIP=`ifconfig | grep -A 1 eth0 | grep inet | cut -f 2 -d "t" | cut -f 2 -d " "`

sudo docker rmi devico-coins

sudo docker build -t devico-coins .

sudo INT=$MYIP docker compose up -d


echo "checkout the api docs at: $MYIP:80/docs"
echo "checkout the graphql at: $MYIP:80/graphql"
echo "checkout the rabbitmq status at: $MYIP:15672 with the user: guest and the password: guest"
