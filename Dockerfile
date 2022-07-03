# base python
FROM python:3.8

# set default port
EXPOSE 8501

# set huggingface env
ENV HF_HOME=/huggingface_models
ENV TRANSFORMERS_CACHE=${HF_HOME}/transformers

# create workdir
WORKDIR /Digest

# copy source
COPY . /Digest

# update and pip install
RUN apt-get update && \
    pip3 install -r requirements.txt

# set command
CMD streamlit run app.py
