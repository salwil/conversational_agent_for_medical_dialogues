import setuptools

setuptools.setup(name='conversation',
version='1.0',
description='Conversation Package',
url='https://github.com/salwil/conversational_agent_for_medical_dialogues',
author='Salome Wildermuth',
python_requires='>=3.8',
install_requires=[
    'en_core_web_sm'
],
entry_points={
        'console_scripts': [
            'mda = conversation.main:main']
    },
author_email='salome.wildermuth@uzh.ch',
packages=setuptools.find_packages())