FROM ubuntu:18.04
ENTRYPOINT []
# RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==1.10.8 && pip3 install --no-cache rasa[transformers] && pip3 install --no-cache pandas==1.1.0
RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==1.10.8 && pip3 install --no-cache pandas==1.1.0 && pip3 install --no-cache rasa[spacy] && python3 -m spacy download en_core_web_md && python3 -m spacy link en_core_web_md en 

ADD . /app/
EXPOSE 5055
RUN chmod +x /app/actionserver/start_services.sh
CMD /app/actionserver/start_services.sh