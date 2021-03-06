export MYIP=`ifconfig | grep -A 1 eth0 | grep inet | cut -f 2 -d "t" | cut -f 2 -d " "`

docker rmi devico-coins

docker build -t devico-coins .

docker compose down -v
docker compose up -d

if [ $MYIP ]; then
    echo "checkout the api docs at: http://$MYIP:8000/docs"
else
    echo "checkout the api docs at: http://127.0.0.1:8000/docs"
fi
if [ $MYIP ]; then
    echo "checkout the graphql at: http://$MYIP:8000/graphql"
else
    echo "checkout the graphql at: http://127.0.0.1:8000/graphql"
fi
if [ $MYIP ]; then
    echo "checkout the rabbitmq status at: http://$MYIP:15672 with the user: guest and the password: guest"
else
    echo "checkout the rabbitmq status at: http://127.0.0.1:15672 with the user: guest and the password: guest"
fi
