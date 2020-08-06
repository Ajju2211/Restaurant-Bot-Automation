cd app/
# Start rasa server with nlu model

# rasa run --model models --enable-api \
#         --endpoints endpoints.yml \
#         --credentials credentials.yml \
#         -p $PORT
rasa run --model models --enable-api --cors "*" --debug \
         -p $PORT