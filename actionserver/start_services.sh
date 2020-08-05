cd app/
# Start rasa actions server 
# rasa run actions --actions app.actions --enable-api --cors "*" --debug \
#          -p $PORT_ACTION_SERVER
# rasa run actions -p $PORT_ACTION_SERVER
rasa run actions --actions app.actions
