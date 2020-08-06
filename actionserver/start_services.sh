cd app/
# Start rasa actions server 
# rasa run actions --actions app.actions  --cors "*" --debug \
#          -p $PORT
rasa run actions --actions actions --cors "*" --debug -p $PORT
            
