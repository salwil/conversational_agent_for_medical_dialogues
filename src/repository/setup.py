import setuptools

setuptools.setup(name='repository',
version='1.0',
description='Repository Package',
url='https://github.com/salwil/conversational_agent_for_medical_dialogues',
author='Salome Wildermuth',
python_requires='>=3.8',
install_requires=[],
author_email='salome.wildermuth@uzh.ch',
packages=setuptools.find_packages(),
data_files=[('conversation/repository/data', ['data/mental_states_with_intros.csv',
                                 'data/more_detail_questions.csv',
                                 'data/profile_questions.csv',
                                 'data/questions_for_topics_10.csv'])]
)