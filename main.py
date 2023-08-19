import gradio as gr
from answer_generation import generate_output
import time

def make_gradio():
    examples = [
        ['Tower of London'],
        ['Le Louvre'],
        ['MoMA'],
        ['Eiffel Tower'],
        ['Sagrada Familia'],
    ]
    with gr.Blocks(title="AccessLLM", theme=gr.themes.Base(primary_hue="blue")) as iface:
        with gr.Column():
            head = gr.Markdown("""# AccessLLM
            AccessLLM is a tool that helps people with disability to find accessibility information about places they want to visit. AccessLLM is completely open-source and is not a commercial product. Also the technology used (large language models) can in some cases generate unseen informations. Please treat the provided output carefully.""")
            
            
            with gr.Row():
                inputs = gr.Textbox(lines=1, label="I want some accessibility information about ", placeholder="Enter the place's name here")
                examples = gr.Examples(inputs=inputs, examples=examples)
            with gr.Row():
                btn = gr.Button(value="Search Information", variant="primary")
            with gr.Row(visible=True) as outputs_row:
                outputs = gr.Textbox(label="Accessiblity Information")

            def get_info(inputs, progress=gr.Progress()):
                progress(0.5, desc="Processing...")
                time.sleep(4)
                return {
                    outputs : generate_output(inputs),
                    btn : gr.update(value="Search again!")
                }
            btn.click(fn=get_info, inputs=[inputs], outputs=[outputs, outputs_row, btn])

            footer = gr.Markdown("""
        
        
                For any feedback, inquiry or bug report please contact me through [LinkedIn](https://www.linkedin.com/in/yannis-tevissen/) or [X](https://twitter.com/yannistevissen) or on the [github project page](https://github.com/YannisTevissen/AccessLLM).""")
    iface.queue()
    iface.launch(share=True, width=60, favicon_path="assets/accessllm_favicon.ico")

    return None




if __name__ == '__main__':
    make_gradio()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
