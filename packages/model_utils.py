# custom libs
from . import constants
from . import hardware


def gen_model_selection():
    # determine maximum available memory (in gigabytes)
    mem_size = hardware.available_memory()

    # get compatible model list based on model size and memory size
    return (model for model, info in constants.DEFAULT_MODELS.items() \
            if info['size_gb'] < mem_size)
