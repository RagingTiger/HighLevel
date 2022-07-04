from multiprocessing import Queue, Process
import streamlit as st
import transformers

# custom libs
from packages import model_utils


# configuring page
st.set_page_config(
     initial_sidebar_state="collapsed"
)

# creating sidebar
with st.sidebar:
    # set title
    st.title('Configuration')

    # display example text
    st.header('Example Input Data')
    example_input_dtype = st.selectbox(
        'Input data type',
        ['Text']
    )
    display_example = st.checkbox('Display example input data')

    # create custom model
    st.header('Custom Model')
    model_repo_id = st.text_input('Repo Id'),
    model_name = st.text_input('Name', placeholder='(optional)')
    model_size = st.number_input('Size in GB', value=1.0)

    # create update button
    update_model_button = st.button('Add Model')

    # check for update
    if update_model_button:
        # as long as repo id config it
        if model_repo_id:
            # set name to repo id if it does not exist
            model_name = model_name if modle_name else model_repo_id

            # now update models
            model_utils.constants.DEFAULT_MODELS[model_name] = {
                'repo_id': model_repo_id,
                'size_gb': model_size if model_size else 1,
                'class': 'large' if model_size >= 1 \
                                 else 'medium' if model_size > 0.5 \
                                 else 'small'
            }

        # notify of update succeeding
        st.success('Update successful!')

    # load custom model exec code
    st.header('Custom Execution Code')
    use_custom_code = st.checkbox('Use custom code')

    # get custom model code if any
    if use_custom_code:
        # get custom code
        model_exec_code = st.text_area(
            '',
            placeholder='# custom model exec code here'
        )

        # create exec button
        update_model_exec_code_button = st.button('Update code')

        # check if update needed
        if update_model_exec_code_button:
            # cdisplay ustom model_exec func
            st.write(model_exec_code)

    # clear model/data cache
    st.header('Model/Data Cache')
    clear_cache_auto = st.checkbox('Clear cache automatically')
    clear_cache_now_button = st.button('Clear Cache ')

    # check clear button
    if clear_cache_now_button:
        deploy_model.clear()

# setting unique model_exec code
if not use_custom_code:
    def default_huggingface_pipeline(task, hf_repo_id, input_data):
        # using defalut huggingface python code
        pipe = transformers.pipeline(task, model=hf_repo_id)

        # evalute pipe
        return pipe(input_data)

    # set executing model to default
    model_exec = default_huggingface_pipeline

def inference_process(queue, **parameters):
    # now run inference and store result in IPC queue
    queue.put(model_exec(*parameters))

@st.experimental_memo
def deploy_model(**parameters):
    # setup process queue
    proc_queue = Queue()

    # setup process
    deploy_proc = Process(
        target=inference_process,
        args=(proc_queue, parameters)
    )

    # now start and wait
    deploy_proc.start()
    result = proc_queue.get()
    deploy_proc.join()

    # return contents of queue
    return result


# set title
st.title('High Level')

# select a task
inference_task = st.selectbox(
    'Task', [
        'audio-classification',
        'automatic-speech-recognition',
        'conversational',
        'feature-extraction',
        'fill-mask',
        'image-classification',
        'image-segmentation',
        'object-detection',
        'question-answering',
        'summarization',
        'table-question-answering',
        'text-classification',
        'text-generation',
        'text2text-generation',
        'token-classification',
        'translation',
        'visual-question-answering',
        'zero-shot-classification',
        'zero-shot-image-classification'
    ],
    index=9
)

# select model
model = st.selectbox('Model', model_utils.gen_model_selection())

# get text
txt = st.text_area(
    '',
    height=300,
    placeholder='Enter text here ...',
    value=model_utils.constants.EXAMPLE_TEXT if display_example else ''
)
submit_button = st.button('Submit')

# check button
if not submit_button:
    # stop streamlit execution
    st.stop()

# now summarize
if txt:
    # start and wait for finish
    with st.spinner('Model executing ...'):
        inference_result = deploy_model(
            task=inference_task,
            repo_id=model_utils.constants.DEFAULT_MODELS[model]['repo_id'],
            input_data=txt
        )
        st.success('Inference complete!')
        st.write(inference_result)

# clear cache automatically
if clear_cache_auto:
    deploy_model.clear()
