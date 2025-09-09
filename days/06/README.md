## Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<your-username>/10-day-ai-build-sprint/blob/main/days/06/advanced_rag.ipynb) 
## Advanced RAG Notebook

This README explains how to run and adapt `advanced_rag.ipynb`, which demonstrates a Retrieval-Augmented Generation (RAG) pipeline using LangChain, Chroma vector store, Hugging Face Inference API embeddings, a cross-encoder re-ranker, and an open-source LLM.

### What the notebook does
- Loads and chunks a PDF using `PyPDFLoader` and `RecursiveCharacterTextSplitter`.
- Builds embeddings via `HuggingFaceInferenceAPIEmbeddings` (model `thenlper/gte-large`).
- Indexes chunks in Chroma for similarity search.
- Re-ranks results with a cross-encoder (`BAAI/bge-reranker-base`).
- Generates answers using `HuggingFaceHub` LLM (`HuggingFaceH4/zephyr-7b-alpha`) and a simple LCEL chain.

### Requirements
- Python 3.10+
- Internet access (downloads models and dependencies)
- A Hugging Face access token for:
  - Inference API embeddings
  - Model downloads (optional for public models, but recommended)

Create a token in your Hugging Face settings, then keep it handy.

### Install dependencies
Run these cells at the top of the notebook (already present):

```python
!pip install langchain-community chromadb
!pip install langchain pypdf
!pip install sentence-transformers
```

If you use a local environment (not Colab), prefer a virtual environment and run the same commands in your shell.

### Set your Hugging Face token
In the notebook, run the cell that prompts for your token:

```python
from getpass import getpass
HF_TOKEN = getpass("Enter HF Token:")
import os
os.environ['HUGGINGFACEHUB_API_TOKEN'] = HF_TOKEN
```

Alternatively, set `HUGGINGFACEHUB_API_TOKEN` in your environment before launching Jupyter.

### Provide your document
Update the loader path to your PDF (replace `toncv.pdf` with your file):

```python
documents = PyPDFLoader("/path/to/your.pdf").load()
```

Ensure the file path is correct relative to the notebook.

### Running the pipeline
1. Run install cells.
2. Run the token/auth cell to set `HF_TOKEN` and env var.
3. Run the imports cell before any usage to avoid `NameError`.
4. Update the PDF path and run the data loading/chunking cell.
5. Build embeddings and Chroma index.
6. Create the retriever and re-ranker.
7. Configure the LLM and prompt.
8. Set `query` and run the LCEL chain to get a response.

### Query example
```python
query = "What is the owner contributions"
response = chain.invoke(query)
print(response)
```

### Notes and caveats
- Large downloads: `BAAI/bge-reranker-base` will download ~1.1 GB on first use.
- Colab warnings: If you see warnings about missing Colab secrets for `HF_TOKEN`, it means you typed it at runtime. That is fine for public models; a token is recommended.
- PyPDFLoader NameError: Run the imports cell first: `from langchain_community.document_loaders import PyPDFLoader`.
- CPU-only runs: All components can run on CPU, but re-ranking and LLM calls may be slow. Consider smaller models if needed.
- Chroma persistence: This notebook uses in-memory Chroma. For persistence, pass `persist_directory` to `Chroma.from_documents(...)` and call `db.persist()`.

### Customize
- Change the embedding model in `HuggingFaceInferenceAPIEmbeddings` if desired.
- Adjust `chunk_size` and `chunk_overlap` in `RecursiveCharacterTextSplitter`.
- Tune retrieval `k` and re-ranker `top_n`.
- Swap the LLM in `HuggingFaceHub` to any compatible hosted model.

### Troubleshooting
- "name 'PyPDFLoader' is not defined": The imports cell wasn’t run.
- Authentication errors: Ensure `HUGGINGFACEHUB_API_TOKEN` is set and valid.
- Memory errors during model downloads: Use lighter models or ensure sufficient disk/RAM.
- Slow inference: Reduce `max_new_tokens`, choose smaller models, or use a GPU runtime.

### References
- LangChain docs: `https://python.langchain.com/`
- Chroma docs: `https://docs.trychroma.com/`
- Hugging Face Hub: `https://huggingface.co/`
- bge-reranker: `https://huggingface.co/BAAI/bge-reranker-base`
- Zephyr 7B: `https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha`
