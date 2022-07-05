import transformers

# custom libs
from . import constants
from . import hardware


def gen_model_selection():
    # determine maximum available memory (in gigabytes)
    mem_size = hardware.available_memory()

    # get compatible model list based on model size and memory size
    return (model for model, info in constants.DEFAULT_MODELS.items() \
            if info['size_gb'] < mem_size)

# setting unique model_exec code
def default_huggingface_pipeline(task, hf_repo_id, input_data):
    # using defalut huggingface python code
    pipe = transformers.pipeline(task, model=hf_repo_id)

    # evalute pipe
    return pipe(input_data)

# set executing model to default
model_exec = default_huggingface_pipeline
