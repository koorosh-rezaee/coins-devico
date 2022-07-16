export MYIP=`ifconfig | grep -A 1 eth0 | grep inet | cut -f 2 -d "t" | cut -f 2 -d " "`

sudo docker rmi devico-coins

sudo docker build -t devico-coins .

sudo docker compose up -d

if [ $MYIP ]; then
    echo "checkout the api docs at: http://$MYIP/docs"
else
    echo "checkout the api docs at: http://127.0.0.1:80/docs"
fi
if [ $MYIP ]; then
    echo "checkout the graphql at: http://$MYIP:80/graphql"
else
    echo "checkout the graphql at: http://127.0.0.1:80/graphql"
fi
if [ $MYIP ]; then
    echo "checkout the rabbitmq status at: http://$MYIP:15672 with the user: guest and the password: guest"
else
    echo "checkout the rabbitmq status at: http://127.0.0.1:15672 with the user: guest and the password: guest"
fi
