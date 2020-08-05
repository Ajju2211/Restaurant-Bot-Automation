cd app/
# Start rasa actions server 
# rasa run actions --actions app.actions --enable-api --cors "*" --debug \
<<<<<<< HEAD
#          -p $PORT
rasa run actions -p $PORT
=======
#          -p $PORT_ACTION_SERVER
# rasa run actions -p $PORT_ACTION_SERVER
rasa run actions --actions actions
>>>>>>> 7f5d49db1055e748fd8d13d9b632092b7172e9b5
