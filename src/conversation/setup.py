import setuptools

setuptools.setup(name='conversation',
version='1.0',
description='Conversation Package',
url='https://github.com/salwil/conversational_agent_for_medical_dialogues',
author='Salome Wildermuth',
python_requires='>=3.7',
install_requires=[],
entry_points={
        'console_scripts': [
            'conversation = conversation.main:main'        ]
    },
author_email='salome.wildermuth@uzh.ch',
packages=setuptools.find_packages())