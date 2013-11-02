Précis
======
pronounced "preh-si"

[![Build Status](https://travis-ci.org/machinelearner/precis.png)](https://travis-ci.org/machinelearner/precis)

### Graph Based Multi-Document Text summarization engine with semantic feature weightage.

* Currently the feature weighing is achieved using WordNet, but this will eventually be replaced with word2vec
* Still a lot of performance enhancements required. More tests and more API features to follow

#### Setup
* Install Python 2.7.x
* Install virtualenv to manage packages
* Install packages from eggs.txt
* Install nltk data packages, from prompt execute these

```bash
pip install virtualenv
virtualenv .env # this creates environment for this application
source .env/bin/activate
pip install -r eggs.txt
python nltk_setup.py
```

or Use ```make``` shipped with this project

```bash
make env
source .env/bin/activate
```

#### Usage
* After the setup you can run the following script against a document directory with a list of documents belonging to
similar topic to generate Summary

```bash
./summarize.py <content directory path>
```
#### Running Tests (View Readme in tests)

```bash
make tests
```
