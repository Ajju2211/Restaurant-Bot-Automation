# Restaurant-Bot-Automation

![Push Rasa bot container to Heroku](https://github.com/naaniz/Restaurant-Bot-Automation/workflows/Push%20Rasa%20bot%20container%20to%20Heroku/badge.svg)

![Push action server to heroku](https://github.com/naaniz/Restaurant-Bot-Automation/workflows/Push%20action%20server%20to%20heroku/badge.svg)

#### MODULES LIST (append here)

```sh
$ pip3 install  rasa==1.10.8
$ pip3 install rasa[spacy]
$ python -m spacy download en_core_web_md
$ python -m spacy link en_core_web_md en
$ pip3 install  pandas==1.1.0
$ pip3 install fuzzywuzzy==0.18.0
$ pip3 install python-levenshtein==0.12.0  *** for linux and other docker, os ***
```
```powershell
cmd:\ conda install -c conda-forge python-levenshtein==0.12.0  *** for windows only ***
```

#### SETUP
- Create conda environment and create project in this environment
- After installing requirements above
- Add current working directory of this project in your python environment variable eg: PATH = D:\Projects\...\Restaurant-Bot-Automation
- Go to Anaconda3\envs\rasa\Lib\site-packages\rasa\core\channels\console.py and set DEFAULT_STREAM_READING_TIMEOUT_IN_SECONDS=100 
#### TASK DONE
- [ ] Complaints 
    - [ ] Back button in complaints 
    - [x] Saving complaints 
    - [x] Able to save anything
- [ ] Feedbacks
    - [ ] Back button
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
- [ ] home menu showing options
    - [ ] Back in home menu
    - [ ] included Faq's
    - [x] included Ordering
    - [x] included queries (complaints/Feedbacks)
    


License
----

MIT
