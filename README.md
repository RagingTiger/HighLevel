# TL;DR
A web-based high-level interface that allows you to summarize documents,
websites, and any text of your choosing.

## Deploy
To deploy the *streamlit app* with **Docker**:
```
docker run -d \
           --name digest \
           -v digest_models:/huggingface_models \
           -p 8501:8501 \
           ghcr.io/ragingtiger/digest:master
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
    simply run `docker logs -f digest` to see them.
