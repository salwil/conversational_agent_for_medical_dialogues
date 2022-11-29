# conversational_agent_for_medical_dialogues
<div id="top"></div>

## About
This medical dialogue agent (MDA) is designed to assist in clinical consultation in the orofacial complaints domain.
The MDA is a hybrid system, consisting of transformer- probability- and rulebased
question generation. The dialogue management consists of finite-state, frame-based
as well as agent-based components. The MDA is responsible to lead the conversation,
it is a system-initiative architecture. The MDA is a task-oriented dialogue
agent. The implemented rules as well as the predetermined questions and sentence
parts are aligned exclusively to the topic of orofacial pains.

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting started
### Prerequisites
- Python 3.8 installed

<p align="right">(<a href="#top">back to top</a>)</p>

## Installation in virtual environment

- Open the command line window
- Clone the repository with  
  `>> git clone git@github.com:salwil/conversational_agent_for_medical_dialogues.git`
- Visit the root directory:  
  `>> cd conversational_agent_for_medical_dialogues`
- Create a virtual environment with Python >= 3.8:  
  `>> python3.8 -m venv venv`
- Activate the virtual environment:  
  `source venv/bin/activate`
- Install the following Python packages with command:  
  `>> pip3.8 install transformers==4.24.0`  
  `>> pip3.8 install spacy==3.4.3`  
  `>> python3.8 -m spacy download en_core_web_sm`  
  `>> pip3.8 install torch==1.13.0`  
  `>> pip3.8 install nltk==3.7`  
  `>> pip3.8 install en_core_web_sm`  
  `>> pip3.8 install sentencepiece==0.1.97`  
- Go to the src directory:  
  `cd src`
- Install the MDA packages:  
  `>> pip3.8 install conversation/`  
  `>> pip3.8 install conversation_turn/`  
  `>> pip3.8 install helpers/`  
  `>> pip3.8 install model/`  
  `>> pip3.8 install preprocess/`  
  `>> pip3.8 install repository/`  
  `>> pip3.8 install rules/`  
- Go back to the root directora and run the unittests before you start, to make sure, everything is setup correctly (this may take 2-3 minutes):  
  `>> python3.8 -m unittest tests/*/*_test.py`  
  In the end you should see something like `Ran 49 tests in xxx.xxxs` without any errors.

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage
The system is ready to use without doing any special configurations. But they are default configurations.
If you want to set the system up according to specific needs, follow the instructions in the
<a href="#configurability">Configurability</a> chapter.
- Command to start a new conversation:  
  `>> conversation`
- Command to terminate a running conversation:  
  `>> q!` or `>> quit!`

<p align="right">(<a href="#top">back to top</a>)</p>

## Configurability
<div id="configurability"></div>

**Important Note:** To make changes in the configuration active, the repository package has to be installed again with
`>> pip3.8 install repository/`

### Add profile questions
- Profile questions have to be added in the `src/repository/data` folder in a csv file called `profile_questions.csv`. 
- The first column contains the question in english, the third column contains the question in German. The second column
contains the identifier `profile`.
- All three columns are mandatory fields.
- The csv columns are delimited by tabulator quote character is `"` 
- You can work with the default inventory of questions or you can add, remove and change entries, but make sure, there is at least one entry in the file and that you do not delete the file. Otherwise the system may
behave unpredictable

### Add mental states and empathic phrases
- Empathic phrases have to be added in the `src/repository/data` folder in a csv file called `mental_states_with_intros.csv`.
- The first column contains a mental state, the second column contains the corresponding empathic phrase in English and 
the third column contains the corresponding empathic phrase in German.
- All three columns are mandatory fields.
- The csv columns are delimited by tabulator quote character is `"` 
- You can work with the default inventory of mental states and empathic phrases or you can add, remove and change entries,
but make sure, there is at least one entry in the file and that you do not delete the file. Otherwise the system may
behave unpredictable

### Add questions that ask for more details
- Empathic phrases have to be added in the `src/repository/data` folder in a csv file called `more_detail_questions.csv`.
- The first column contains the question in English, the second column contains the corresponding empathic phrase in
German
- Both columns are mandatory fields.
- The csv columns are delimited by tabulator quote character is `"` 
- You can work with the default inventory of more-detail questions or you can add, remove and change entries, 
but make sure, there is at least one entry in the file and that you do not delete the file. Otherwise the system may
behave unpredictable

### Add topic questions
- Topic questions have to be added in the `src/repository/data` folder in a csv file called `questions_for_topics_x.csv`,
with x referring to the number of topics from the linked topic model.
- The first column contains the topic number, the second column contains the question in English and the third column 
contains the question in German.
- All three columns are mandatory fields.
- The csv columns are delimited by tabulator quote character is `"` 
- You can work with the default inventory of questions or you can add, remove and change entries, but make sure, there is at least one entry in the file and that you do not delete the file. Otherwise the system may
behave unpredictable
### Add more topics
- If you want to use the available topic model but with another number of topics, you have to make a little
change at the code.
- There are 4 different topic lists available in the `src/model/language_models/mallet_topics` folder:
`mallet.topic_keys.5` with 5 topics, `mallet.topic_keys.10` with 10 topics (which is in use
by default), `mallet.topic_keys.15` with 15 and finally `mallet.topic_keys.20` with 20 topics.
- In the `src/conversation/conversation` folder, open the `conversation.py` file and change the value
`number_of_pretrained_topics` parameter in the `TopicInferencer` instantiation line.
- If you add a `questions_for_topics_x.csv` file with the correct number of topics in the name
  (what is recommended), the filename also has to be updated accordingly in the `load_data_into_repo.py` file
in the `src/repository/repository` folder.
- Do not forget to reinstall the conversation package, after the changes have been saved.

### Add new topic model
- If you want to add a new trained topic model, you have to add it in the `src/model/language_models/mallet_topics`
folder.
- By adding a new topic model, even if the same number of topics is used as in the previous
configuration, the file with the topic questions should be revised. The topic numbers have other
topics in a new topic model and are probably distributed differently (assuming other data was used
train the new model)

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact
Salome Wildermuth, [salome.wildermuth@uzh.ch](salome.wildermuth@uzh.ch)  
Project Link: https://github.com/salwil/conversational_agent_for_medical_dialogues  
Template: https://github.com/othneildrew/Best-README-Template/blob/master/README.md

<p align="right">(<a href="#top">back to top</a>)</p>

## References

<p align="right">(<a href="#top">back to top</a>)</p>

