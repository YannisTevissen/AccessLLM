from crawler import get_all_urls
from llama_index import ListIndex, SimpleWebPageReader
import openai
import os
import gradio as gr
from places import find_place_from_name


keywords = ['handicap', 'pmr', 'acces', 'disable', 'disability', 'pratique', 'practical', 'venu', 'venir']

def answer_question(url: str, question: str):
    openai.api_key = os.environ['OPEN_AI_API_KEY']
    urls = get_all_urls(url, keywords)
    if url not in urls:
        urls.append(url)
    documents = SimpleWebPageReader(html_to_text=True).load_data(
        urls
    )
    index = ListIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    print(
        response
    )
    return response


def make_gradio():
    examples = [
        ['Telecom SudParis'],
        ['Le Louvre'],
        ['Les Catacombes de Paris'],
        ['Les 500 diables'],
    ]
    with gr.Blocks(title="AccessLLM") as iface:
        with gr.Row():
            inputs = gr.Textbox(lines=1, label="I want some accessibility information about ", placeholder="Enter the place's name here")
            examples = gr.Examples(inputs=inputs, examples=examples)
            lang = gr.Dropdown(label="Language", choices=["English", "French"])
        with gr.Row():
            btn = gr.Button("Process website", variant="primary")
        with gr.Row():
            outputs = gr.Textbox(label="Accessiblity Information")

        btn.click(fn=generate_output, inputs=[inputs, lang], outputs=outputs)


    iface.launch(debug=False)
    return None


def generate_output(input_text, lang):

    place_dict = find_place_from_name(input_text)
    url = place_dict['places'][0]['websiteUri']
    name = place_dict['places'][0]['displayName']['text']
    address = place_dict['places'][0]['formattedAddress']

    if lang == "English":
        default_prompt = "What are the indications for people with disability coming to this place? If none don't make it up."
    elif lang == "French":
        default_prompt = "Quelles sont les indications pour les personnes handicapées venant dans ce lieu ? Si aucun, ne l'inventez pas."
    else:
        default_prompt = "What are the indications for people with disability coming to this place? If none don't make it up."
    information = answer_question(url, default_prompt)
    answer = f"""{name}\n {address} \n\n{information}"""
    return answer



if __name__ == '__main__':
    make_gradio()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
