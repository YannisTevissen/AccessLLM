import gradio as gr
from answer_generation import generate_output
import time

def make_gradio():
    examples = [
        ['Alhambra'],
        ['Le Louvre'],
        ['Grand Canion'],
        ['Les 500 diables'],
    ]
    with gr.Blocks(title="AccessLLM", theme=gr.themes.Base(primary_hue="blue")) as iface:
        with gr.Column():
            head = gr.Markdown("""![banner](https://github.com/YannisTevissen/AccessLLM/blob/main/assets/accessllm_banner.png)""")
            with gr.Row():
                inputs = gr.Textbox(lines=1, label="I want some accessibility information about ", placeholder="Enter the place's name here")
                examples = gr.Examples(inputs=inputs, examples=examples)
                lang = gr.Dropdown(label="Language", choices=["English", "French"])
            with gr.Row():
                btn = gr.Button(value="Search Information", variant="primary")
            with gr.Row(visible=False) as outputs_row:
                outputs = gr.Textbox(label="Accessiblity Information")

            def get_info(inputs, lang, progress=gr.Progress()):
                progress(0.5, desc="Processing...")
                time.sleep(4)
                return {
                    outputs_row : gr.update(visible=True),
                    outputs : generate_output(inputs, lang),
                    btn : gr.update(value="Search again!")
                }
            btn.click(fn=get_info, inputs=[inputs, lang], outputs=[outputs, outputs_row, btn])


    iface.launch(enable_queue=True, share=True, width=60, favicon_path="https://github.com/YannisTevissen/AccessLLM/blob/main/assets/accessllm_favicon.ico")
    return None




if __name__ == '__main__':
    make_gradio()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
