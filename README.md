# Restaurant-Bot-Automation

![Push Rasa bot container to Heroku](https://github.com/naaniz/Restaurant-Bot-Automation/workflows/Push%20Rasa%20bot%20container%20to%20Heroku/badge.svg)

![Push action server to heroku](https://github.com/naaniz/Restaurant-Bot-Automation/workflows/Push%20action%20server%20to%20heroku/badge.svg)

#### MODULES LIST (append here!)

```sh
$ pip3 install  rasa==1.10.8
$ pip3 install rasa[spacy]
$ python -m spacy download en_core_web_md
$ python -m spacy link en_core_web_md en
$ pip3 install  pandas==1.1.0
$ pip3 install  nltk==3.5
$ pip3 install fuzzywuzzy==0.18.0
$ pip3 install python-levenshtein==0.12.0  *** for linux and other docker, os ***
```
```powershell
cmd:\ conda install -c conda-forge python-levenshtein==0.12.0  *** for windows only ***
```

#### Extra SETUP
- Create conda environment and create project in this environment
- After installing requirements in above Modules LIST
- To add custom component to rasa
    -   Add current working directory of this project in your python environment variable      -   eg: PATH = D:\Projects\...\Restaurant-Bot-Automation
- To set the console channel Timeout in seconds
    -  Go to Anaconda3\envs\{your_rasa_env}\Lib\site-packages\rasa\core\channels\console.py
    -  And set DEFAULT_STREAM_READING_TIMEOUT_IN_SECONDS=200 

#### How to Train ?
- ##### To use default Rasa configs
```sh
$ rasa train
```
- ##### To use spacy config pipeline (Fast to train)
```sh
$ rasa train -c spacy_config.yml
```

#### How to run 
- ##### To run action server
```sh
$ rasa run actions --actions actionserver.actions
```
- ##### To run rasa in debug mode to inspect slot filling and entities ..,
```sh
$ rasa shell --debug
```
- ##### To run rasa in normal shell
```sh
$ rasa shell
```



#### TASK DONE
- [ ] Complaints 
    - [x] Back button in complaints 
    - [x] Saving complaints 
    - [x] Able to save anything
- [ ] Feedbacks
    - [x] Back button
    - [x] Saving feedbacks
    - [x] Able to save anything
- [ ] Ordering 
    - [ ] Back buttons
        - [x] Back button to change dish after selecting
        - [ ] Back buttons everywhere
    - [x] Able to search any dish
    - [x] Menu image based 
    - [ ] Category wise ordering
    - [ ] Explore Dishes by displaying Carousels
    - [ ] Sorts
        - [ ] Sort by price
        - [ ] Sort by names
        - [ ] Sort by rating 
        - [ ] Sort by nearest location
        - [ ] Sort by popular dish 
    - [ ] Filters 
        - [ ] price range
        - [ ] location
        - [ ] Rating
- [ ] Faqs
    - [x] Back in Faqs
    - [x] Search question
    - [x] Select Queston (collapsible button)
- [ ] home menu showing options
    - [ ] Back in home menu
    - [x] included Faq's
    - [x] included Ordering
    - [x] included queries (complaints/Feedbacks)
    

License
----
Apache License 2.0
