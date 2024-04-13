# IPL-2024-Auction-Q&ABot-RAG-LLM
This repository contains code for creating Q&Abot using RAG &amp; LLM which can answer questions regarding IPL 2024 Auctions.

![rag-video](./docs/streamlit-extended.gif)

### LLM Used
In this app I have used `google/flan-t5-small` model which can be run locally.

### Embeddings Used
For creating document and question embeddings I have used `bge-base-en-v1.5` embedding model.

### How to run this code
```python
# Create virtual env
conda create -n ipl2024_rag python=3.11
conda activate ipl2024_rag

# Install necessary dependencies
pip install -r requirement_local.txt

# Run the streamlit app
streamlit run app.py

```

### System Configuration
This RAG based bot is running on `Macbook Air (16GB RAM)`