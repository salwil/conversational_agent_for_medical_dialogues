import setuptools

setuptools.setup(name='preprocess',
version='1.0',
description='Preprocess Package',
url='https://github.com/salwil/conversational_agent_for_medical_dialogues',
author='Salome Wildermuth',
python_requires='>=3.8',
install_requires=[
    'nltk==3.7',
    'spacy==3.4.3',
    'en_core_web_sm'
],
author_email='salome.wildermuth@uzh.ch',
packages=setuptools.find_packages())