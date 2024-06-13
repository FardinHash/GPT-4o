import gradio as gr

# Import modules from other files
from bot import chatbot, model_inference, BOT_AVATAR, EXAMPLES, model_selector, decoding_strategy, temperature, max_new_tokens, repetition_penalty, top_p
from voice import respond
from chat import videochat

# Define Gradio theme
theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="orange",
    neutral_hue="gray",
    font=[gr.themes.GoogleFont('Libre Franklin'), gr.themes.GoogleFont('Public Sans'), 'system-ui', 'sans-serif']
).set(
    body_background_fill_dark="#111111",
    block_background_fill_dark="#111111",
    block_border_width="1px",
    block_title_background_fill_dark="#1e1c26",
    input_background_fill_dark="#292733",
    button_secondary_background_fill_dark="#24212b",
    border_color_primary_dark="#343140",
    background_fill_secondary_dark="#111111",
    color_accent_soft_dark="transparent"
)


# Chat interface block
with gr.Blocks(
        fill_height=True,
        css=""".gradio-container .avatar-container {height: 40px width: 40px !important;} #duplicate-button {margin: auto; color: white; background: #f1a139; border-radius: 100vh; margin-top: 2px; margin-bottom: 2px;}""",
) as chat:
    gr.Markdown("# Image Chat, Image Generation, Image classification and Normal Chat")
    with gr.Row(elem_id="model_selector_row"):
        # model_selector defined in chatbot.py
        pass  
    # decoding_strategy, temperature, top_p defined in chatbot.py
    decoding_strategy.change(
        fn=lambda selection: gr.Slider(
            visible=(
                    selection
                    in [
                        "contrastive_sampling",
                        "beam_sampling",
                        "Top P Sampling",
                        "sampling_top_k",
                    ]
            )
        ),
        inputs=decoding_strategy,
        outputs=temperature,
    )
    decoding_strategy.change(
        fn=lambda selection: gr.Slider(visible=(selection in ["Top P Sampling"])),
        inputs=decoding_strategy,
        outputs=top_p,
    )
    gr.ChatInterface(
        fn=model_inference,
        chatbot=chatbot,
        examples=EXAMPLES,
        multimodal=True,
        cache_examples=False,
        additional_inputs=[
            model_selector,
            decoding_strategy,
            temperature,
            max_new_tokens,
            repetition_penalty,
            top_p,
            gr.Checkbox(label="Web Search", value=True),
        ],
    )

# Voice chat block
with gr.Blocks() as voice:
    with gr.Row():
        select = gr.Dropdown(['Nous Hermes Mixtral 8x7B DPO', 'Mixtral 8x7B', 'StarChat2 15b', 'Mistral 7B v0.3',
                              'Phi 3 mini', 'Zephyr 7b'], value="Mistral 7B v0.3", label="Select Model")
        seed = gr.Slider(
            label="Seed",
            minimum=0,
            maximum=999999,
            step=1,
            value=0,
            visible=False
        )
        input = gr.Audio(label="User", sources="microphone", type="filepath", waveform_options=False)
        output = gr.Audio(label="AI", type="filepath",
                          interactive=False,
                          autoplay=True,
                          elem_classes="audio")
        gr.Interface(
            fn=respond,
            inputs=[input, select, seed],
            outputs=[output], api_name="translate", live=True)

# Live chat block
with gr.Blocks() as livechat:
    gr.Interface(
        fn=videochat,
        inputs=[gr.Image(type="pil",sources="webcam", label="Upload Image"), gr.Textbox(label="Prompt", value="what he is doing")],
        outputs=gr.Textbox(label="Answer")
    )


# Main application block
with gr.Blocks(theme=theme, title="Open Source GPT-4o") as demo:
    gr.Markdown("# GPT-4o")
    gr.TabbedInterface([chat, voice, livechat], ['💬 SuperChat','🗣️ Voice Chat','📸 Live Chat'])

demo.queue(max_size=300)
demo.launch()