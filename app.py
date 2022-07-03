from multiprocessing import Queue, Process
import streamlit as st
import transformers

# custom libs
from packages import model_utils


def inference_process(task, repo_id, txt, queue):
    # using huggingface pipeline to autodownload and prepare model
    pipe = transformers.pipeline(task, model=repo_id)

    # now run inference and store result in IPC queue
    queue.put(pipe(txt))

@st.experimental_memo
def deploy_model(*parameters):
    # setup process queue
    proc_queue = Queue()

    # setup process
    deploy_proc = Process(
        target=inference_process,
        args=(*parameters, proc_queue)
    )

    # now start and wait
    deploy_proc.start()
    result = proc_queue.get()
    deploy_proc.join()

    # return contents of queue
    return result

# configuring page
st.set_page_config(
     initial_sidebar_state="collapsed"
)

# creating sidebar
with st.sidebar:
    # set title
    st.title('Advanced Config')

    # display example text
    st.header('Example Text')
    display_example = st.checkbox('Display example text')

    # create custom model
    st.header('Custom Model')
    repo_id = st.text_input('Repo ID')
    name = st.text_input('Name (optional)')
    size_gb = st.number_input('Size in GB (optional)')

    # create update button
    update_button = st.button('Update')

    # check for update
    if update_button:
        # as long as repo id config it
        if repo_id:
            # set name to repo id if it does not exist
            model_name = name if name else repo_id

            # now update models
            model_utils.constants.DEFAULT_MODELS[model_name] = {
                'repo_id': repo_id,
                'size_gb': size_gb if size_gb else 1,
                'class': 'large' if size_gb >= 1 \
                                 else 'medium' if size_gb > 0.5 \
                                 else 'small'
            }

        # notify of update succeeding
        st.success('Update successful!')

    # clear model/data cache
    st.header('Model/Data Cache')
    clear_cache_auto = st.checkbox('Clear cache automatically')
    clear_cache_now_button = st.button('Clear Cache ')

    # check clear button
    if clear_cache_now_button:
        deploy_model.clear()


# set title
st.title('Digest')

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
    # get repo id
    repo_id = model_utils.constants.DEFAULT_MODELS[model]['repo_id']

    # start and wait for finish
    with st.spinner('Model executing ...'):
        summary = deploy_model('summarization', repo_id, txt)
        st.success('Summary complete!')
        st.write(summary)

# clear cache automatically
if clear_cache_auto:
    deploy_model.clear()
