sudo docker rmi devico-coins

sudo docker build -t devico-coins .

sudo docker compose up -d


echo "checkout the api docs at: http://127.0.0.1:80/docs"
echo "checkout the graphql at: http://127.0.0.1:80/graphql"
echo "checkout the rabbitmq status at: http://127.0.0.1:15672 with the user: guest and the password: guest"
