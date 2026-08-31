# GPT-4o

![logo](logo.png)

GPT-4o provides a local Gradio interface for Hugging Face hosted chat models. The
application does not download or load a large model at startup; generation is
performed through the Hugging Face Inference API.

## Setup

1. Create and activate a Python 3.10 or later virtual environment.
2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Create a Hugging Face access token and make it available as `HF_TOKEN`.
4. Start the application:

   ```sh
   python app.py
   ```

Open the local URL printed by Gradio. Select a hosted model from the dropdown
and send a message.

## Docker

```sh
docker compose up --build
```

Pass `HF_TOKEN` to the container through your shell environment or your
Compose environment configuration.
