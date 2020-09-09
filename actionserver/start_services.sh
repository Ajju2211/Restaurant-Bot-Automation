cd app/
# Start rasa actions server 
# rasa run actions --actions app.actions --enable-api --cors "*" --debug \
#          -p $PORT
rasa run actions --actions app.actions --cors "*" --debug -p $PORT
