import logging
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from service.rag.embedding import get_embedding_function
from schema.llm_dto import LLMResponseDTO, LLMQueryDTO
from config import CHROMA_PATH, GEMINI_KEY, GEMINI_LLM_MODEL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


PROMPT_TEMPLATE = """
You are a chatbot designed to help players understand the rules of the all popular game monopoly.
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""



def get_model():
    return ChatGoogleGenerativeAI(
        google_api_key = GEMINI_KEY,
        model=GEMINI_LLM_MODEL,
        temperature=0,
        timeout=None,
        max_retries=2,
    )


def query_rag(request: LLMQueryDTO) -> LLMResponseDTO :
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(request.query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=request.query_text)
    # print(prompt)

    model = get_model()
    response = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    logging.info(f"Query_ID: {request.query_id} - Sources: {sources}")
    return LLMResponseDTO(
        query_id=request.query_id,
        successful=True,
        query_response=response.content
    )