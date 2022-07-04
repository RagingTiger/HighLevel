# TL;DR
A web-based high-level interface built using [Streamlit](http://streamlit.io)
for developing machine learning models.

## Deploy
To deploy the *streamlit app* with **Docker**:
```
docker run -d \
           --name highlevel \
           -v highlevel_models:/huggingface_models \
           -p 8501:8501 \
           ghcr.io/ragingtiger/highlevel:master
```
Then simply open your browser to `http://localhost:8501` and you should see the
*streamlit* interface.

## FAQ
+ Where are the HuggingFace model downloaded to?
  - The models are downloaded (*cached*) in the `/huggingface_models/transformers` directory, which the docker command in the [deploy](#deploy) section
    manages with *Docker volumes*.

+ Why is my model taking so long to execute?
  - When models are run for the first time, you can expect it will take some time to download from the
    [Model Hub](https://huggingface.co/docs/hub/models-the-hub). You can always monitor the *Docker logs* to see the progress of the *model downloads*,
    simply run `docker logs -f highlevel` to see them.
