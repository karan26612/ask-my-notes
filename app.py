from dotenv import load_dotenv
load_dotenv()
import os
import gradio as gr
from ingest import build_chunks
from store import get_collection, add_chunks
from rag import ask

col = get_collection()


def index_files(files):
    if not files:
        return "No files selected."
    for f in files:
        add_chunks(build_chunks(f, os.path.basename(f)), col)
    return f"Indexed {len(files)} file(s). Total chunks: {col.count()}"


def answer(question):
    if not question or not question.strip():
        return "Please type a question.", ""
    result, hits = ask(question, col=col)
    sources = "\n\n".join(
        f"**{h['file']}, page {h['page']}**\n\n{h['text'][:300]}..." for h in hits
    )
    return result["answer"], sources


with gr.Blocks(title="Ask My Notes", theme=gr.themes.Soft(primary_hue="indigo")) as demo:
    gr.Markdown("# 📚 Ask My Notes\nAsk questions about your PDFs and get answers with page citations.")

    with gr.Row():
        with gr.Column(scale=1):
            files = gr.File(label="Upload PDFs", file_types=[".pdf"], file_count="multiple", type="filepath")
            index_btn = gr.Button("Index documents")
            status = gr.Textbox(label="Status", interactive=False)

        with gr.Column(scale=2):
            q = gr.Textbox(label="Your question", placeholder="e.g. What is a state space?", lines=2)
            ask_btn = gr.Button("Ask", variant="primary")
            ans = gr.Textbox(label="Answer", lines=6)
            with gr.Accordion("Sources", open=False):
                src = gr.Markdown()

    gr.Examples(
        examples=["What is a state space?", "What is breadth-first search?"],
        inputs=q,
    )

    index_btn.click(index_files, files, status)
    ask_btn.click(answer, q, [ans, src])
    q.submit(answer, q, [ans, src])

demo.launch()