import setuptools

setuptools.setup(name='model',
version='1.0',
description='Model Package',
url='https://github.com/salwil/conversational_agent_for_medical_dialogues',
author='Salome Wildermuth',
python_requires='>=3.8',
install_requires=[
    'transformers==4.24.0',
    'torch==1.13.0',
    'en_core_web_sm',
    'sentencepiece==0.1.97'
],
author_email='salome.wildermuth@uzh.ch',
packages=setuptools.find_packages())