from pathlib import Path
import os


def get_project_path():
    path = Path(__file__)
    if os.path.dirname(path).endswith('conversational_agent_for_medical_dialogues'):
        return os.path.dirname(path)
    elif os.path.dirname(path.parent).endswith('conversational_agent_for_medical_dialogues'):
        return os.path.dirname(path.parent)
    elif os.path.dirname(path.parent.parent).endswith('conversational_agent_for_medical_dialogues'):
        return os.path.dirname(path.parent.parent)
    elif os.path.dirname(path.parent.parent.parent).endswith('conversational_agent_for_medical_dialogues'):
        return os.path.dirname(path.parent.parent.parent)
    elif os.path.dirname(path.parent.parent.parent.parent).endswith('conversational_agent_for_medical_dialogues'):
        return os.path.dirname(path.parent.parent.parent.parent)
    elif os.path.dirname(path.parent.parent.parent.parent.parent).endswith('conversational_agent_for_medical_dialoguess'):
        return os.path.dirname(path.parent.parent.parent.parent.parent)
    elif os.path.dirname(path.parent.parent.parent.parent.parent.parent).endswith('conversational_agent_for_medical_dialogues'):
        return os.path.dirname(path.parent.parent.parent.parent.parent.parent)
    else:
        return os.path.dirname((path))

def create_directory_if_not_exists(filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)