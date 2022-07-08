from multiprocessing import Queue, Process
import pkg_resources
import streamlit as st

# custom libs
from packages import model_utils

# user defined custom import statements
if model_utils.custom_imports:
    # get import statements
    exec(model_utils.custom_imports)


# funcs
def inference_process(queue, **parameters):
    # now run inference and store result in IPC queue
    queue.put(model_utils.model_exec(**parameters))

@st.experimental_memo
def deploy_model(**parameters):
    # setup process queue
    proc_queue = Queue()

    # setup process
    deploy_proc = Process(
        target=inference_process,
        args=[proc_queue],
        kwargs=parameters
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
    model_repo_id = st.text_input('Repo Id')
    model_name = st.text_input('Name', placeholder='(optional)')
    model_size = st.number_input('Size in GB', value=1.0)

    # create update button
    update_model_button = st.button('Add Model')

    # check for update
    if update_model_button:
        # as long as repo id config it
        if model_repo_id:
            # set name to repo id if it does not exist
            model_name = model_name if model_name else model_repo_id

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

    # load installed packages
    st.header('Modules')
    st.write('Loaded')
    st.success(
        '  \n'.join(
            sorted(
                [key for key in globals().keys() if not key.startswith('__') \
                 and isinstance(globals()[key], type(st))]
            )
        )
    )

    # load custom import statements
    use_custom_modules = st.checkbox('Import additional modules')

    # show installed
    show_installed_packages = st.checkbox('Show installed packages')

    # if showing
    if show_installed_packages:
        # display
        st.write('Installed')
        st.success(
            '  \n'.join(
                sorted(["%s==%s" % (i.key, i.version) \
                for i in pkg_resources.working_set])
            )
        )

    # clear model/data cache
    st.header('Model/Data Cache')
    clear_cache_auto = st.checkbox('Clear cache automatically')
    clear_cache_now_button = st.button('Clear Cache ')

    # check clear button
    if clear_cache_auto or clear_cache_now_button:
        deploy_model.clear()

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

# check for custom module feature
if use_custom_modules:
    # get custom modules
    custom_import_statements = st.text_area(
        'Custom Import Statements',
        value=model_utils.custom_imports,
        placeholder=model_utils.custom_imports
    )

    # create exec button
    update_modules_button = st.button('Import')

    # check if updating modules
    if update_modules_button:
        # cache import statements
        model_utils.custom_imports = custom_import_statements

        # now reload from top
        st.experimental_rerun()

# get custom model code if any
if use_custom_code:
    # get custom code
    model_exec_code = st.text_area(
        'Custom Model Execution Code',
        placeholder=(
            'def model_exec(**parameters):\n'
            '  # complete this function with your code and return your output\n'
            '  return inference_output'
        )
    )
    # create columns
    col1, col2 = st.columns([1,1])

    # create exec button
    with col1:
        update_model_exec_code_button = st.button('Update')

    # revert if custom code present
    if model_exec_code:
        with col2:
            # create revert button
            revert_to_default = st.button('Load Default')

            # check if reverted
            if revert_to_default:
                # set to default
                model_utils.model_exec = model_utils.default_huggingface_pipeline

                # and clear cache
                st.info('Clearing deploy_model() cache ...')
                deploy_model.clear()

                # notify of default
                st.success('Model execution code reverted to default!')

        # check if update needed
        if update_model_exec_code_button:
            # create new model_exec function
            custom_func = 'def model_exec(**parameters):\n' + \
                ''.join((f'  {line}' for line in model_exec_code.splitlines(True)))

            # define new code
            exec(custom_func)

            # now store in module
            exec('model_utils.model_exec = model_exec')

            # and clear cache
            st.info('Clearing deploy_model() cache ...')
            deploy_model.clear()

            # notify code updated successfully
            st.success('Custom code loaded!')

# get text
user_input = st.text_area(
    'Input Data',
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
if user_input:
    # start and wait for finish
    with st.spinner('Model executing ...'):
        inference_result = deploy_model(
            task=inference_task,
            hf_repo_id=model_utils.constants.DEFAULT_MODELS[model]['repo_id'],
            input_data=user_input
        )
        st.success('Inference complete!')
        st.write(inference_result)
