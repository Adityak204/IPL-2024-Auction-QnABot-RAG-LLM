import pickle

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
    AutoModelForSeq2SeqLM,
)
from langchain.llms import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class LocalRAGllm:
    def __init__(
        self,
        embedding_model_name,
        llm_model_name,
        llm_model_type,
        documents,
        chunk_size=512,
        llm_max_length=1000,
    ):
        self.embedding_model_name = embedding_model_name
        self.llm_model_name = llm_model_name
        self.documents = documents
        self.chunk_size = chunk_size
        self.llm_model_type = llm_model_type
        self.llm_max_length = llm_max_length

    def doc_list_to_langchain_doc(self):
        langchain_docs = []
        for article in self.documents:
            langchain_docs.append(Document(page_content=article))
        self.langchain_docs = langchain_docs

    def splitting_docs_into_chunks(self):
        self.doc_list_to_langchain_doc()
        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            AutoTokenizer.from_pretrained(self.embedding_model_name),
            chunk_size=self.chunk_size,
            chunk_overlap=int(self.chunk_size / 10),
        )
        splits = text_splitter.split_documents(self.langchain_docs)
        return splits

    def __call__(self, user_question):
        # Create chunks
        splits = self.splitting_docs_into_chunks()

        # Create embeddings
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)

        # Vector store
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever()

        # Local LLM setup
        _tokenizer = AutoTokenizer.from_pretrained(self.llm_model_name)
        _model = AutoModelForSeq2SeqLM.from_pretrained(self.llm_model_name)

        pipe = pipeline(
            self.llm_model_type,
            model=_model,
            tokenizer=_tokenizer,
            max_length=self.llm_max_length,
        )

        local_llm = HuggingFacePipeline(pipeline=pipe)

        # Prompt
        template = """
        Given the Context information below, answer the Question. Use only the information from the context. Don’t use any general knowledge.
        Context: {context}

        Question: {question}

        If the answer to the question not available, return the following output : 'This information is not present, kindly search online'
        """

        prompt = ChatPromptTemplate.from_template(template)

        # RAG chain
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | local_llm
            | StrOutputParser()
        )

        return rag_chain.invoke(user_question)
