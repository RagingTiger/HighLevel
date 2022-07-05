# base python
FROM python:3.8

# set default port
EXPOSE 8501

# set huggingface env
ENV HF_HOME=/models/huggingface
ENV TRANSFORMERS_CACHE=${HF_HOME}/transformers

# create workdir
WORKDIR /HighLevel

# copy source
COPY . /HighLevel

# update and pip install
RUN apt-get update && \
    pip3 install -r requirements.txt

# set command
CMD streamlit run app.py
