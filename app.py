import gradio as gr

from bot import DEFAULT_MODEL, MODEL_CHOICES, model_inference


with gr.Blocks(title="GPT-4o") as demo:
    gr.Markdown(
        "# GPT-4o\n\n"
        "A chat interface backed by Hugging Face hosted inference. "
        "Set `HF_TOKEN` before starting the application."
    )
    model_selector = gr.Dropdown(
        choices=MODEL_CHOICES,
        value=DEFAULT_MODEL,
        label="Model",
    )
    gr.ChatInterface(
        fn=model_inference,
        additional_inputs=[model_selector],
        type="messages",
    )


if __name__ == "__main__":
    demo.queue().launch()
