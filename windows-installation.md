# Windows Installation Guide
- Install python 3.7.6
- Install Anaconda 
- Install Visual studio C++ Build Tools Through installing Visual studio Installer [VS_installer](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15)
- go to working directory (eg: d://projects/)

 ```
$ git clone https://github.com/naaniz/Restaurant-Bot-Automation.git
$ cd Restaurant-Bot-Automation
$ conda create -n naaniz-rasa python=3.7.6
$ conda activate naaniz-rasa
$ pip install ujson
$ pip install rasa==1.10.12
$ pip uninstall tensorboard-plugin-wit tensorflow tensorflow-addons tensorflow-estimator tensorflow-hub tensorflow-probability
$ conda install tensorflow==2.1.0
$ pip install rasa[spacy]
$ python -m spacy download en_core_web_md
$ python -m spacy link en_core_web_md en
$ pip uninstall h5py
$ pip install h5py
```
- After above installation steps follow these
- Install requirements from [Modules_list](https://github.com/naaniz/Restaurant-Bot-Automation#modules-list-append-here) here use pip install not pip3 install
- SET UP the extra requirements from here [Extra_Setup](https://github.com/naaniz/Restaurant-Bot-Automation#extra-setup)
- Thats it now you follow the [How_to_train](https://github.com/naaniz/Restaurant-Bot-Automation#how-to-train-) and 
  [How_to_run](https://github.com/naaniz/Restaurant-Bot-Automation#how-to-run) steps.
- 👍 You have done awsome!.

