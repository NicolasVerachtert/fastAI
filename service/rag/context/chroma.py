from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from service.rag.context.embedding import get_embedding_function
import os
import shutil
import logging
from config import CHROMA_PATH, DOCS_PATH
from typing import List
import re

logger = logging.getLogger("app")


def init_chroma(reset: bool) -> None:
    """
    Initializes the Chroma database by processing documents in the local directory.

    Args:
        reset (bool): If True, clears the database before processing.
        
    Returns:
        None
    """
    if reset:
        logger.info("Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents() -> List[Document]:
    """
    Loads documents from the local directory, handling both PDF and TXT formats.

    Returns:
        list: A list of document contents.
    """
    documents = []
    try:
        for file_name in os.listdir(DOCS_PATH):
            file_path = os.path.join(DOCS_PATH, file_name)
            if file_name.endswith('.pdf'):
                loaded_docs = load_from_pdf(file_path)
            elif file_name.endswith('.txt') or file_name.endswith('.md'):
                loaded_docs = load_from_txt(file_path)
            else:
                continue

            for doc in loaded_docs:
                game_mode, language = extract_metadata_from_filename(file_name)
                doc.metadata["game_mode"] = game_mode
                doc.metadata["language"] = language

            documents.extend(loaded_docs)
            
    except FileNotFoundError as e:
        logger.error(f"Documents directory not found: {e}")
    except Exception as e:
        logger.error(f"Error loading documents: {e}")

    return documents


def load_from_pdf(file_path: str) -> List[Document]:
    """
    Loads content from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        list: A list of document content (e.g., pages or sections).
    """
    try:
        logger.info(f"Loading PDF file: {file_path}")
        loader = PyPDFLoader(file_path)
        return loader.load()
    except Exception as e:
        logger.error(f"Error loading PDF file {file_path}: {e}")
        return []


def load_from_txt(file_path: str) -> List[Document]:
    """
    Loads content from a TXT file.

    Args:
        file_path (str): Path to the TXT file.

    Returns:
        list: A list of document content (e.g., pages or sections).
    """
    try:
        logger.info(f"Loading TXT file: {file_path}")
        loader = TextLoader(file_path)
        return loader.load()
    except RuntimeError as e:
        logger.error(f"Error loading TXT file {file_path}: {e}")
        return []


def extract_metadata_from_filename(file_name: str) -> tuple:
    """
    Extracts game_mode and language from the filename in the format `name_game_mode_language.ext`,
    where `ext` can be any file extension.

    Args:
        file_name (str): The name of the file.

    Returns:
        tuple: A tuple (game_mode, language).
    """
    # Regular expression to match the filename pattern: name_game_mode_language.ext (with any extension)
    match = re.match(r".*_(.*?)_(.*?)\.(\w+)$", file_name)
    if match:
        game_mode = match.group(1)  # Extract the game_mode
        language = match.group(2)   # Extract the language
        return game_mode, language
    else:
        logger.warning(f"Filename {file_name} does not match the expected format.")
        return "unknown", "unknown"  # Return default values if the format doesn't match


def split_documents(documents: List[Document]) -> list[Document]:
    """
    Splits documents into smaller chunks for processing.

    Args:
        documents (list): A list of document contents.

    Returns:
        list: A list of document chunks.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=250,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)
    except Exception as e:
        logger.error(f"Error splitting documents: {e}")
        return []


def add_to_chroma(chunks: list[Document]) -> None:
    """
   Adds document chunks to the Chroma database.

   Args:
       chunks (List[Document]): A list of document chunks.

   Returns:
       None
   """
    try:
        # Load the existing database.
        db = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
        )

        # Calculate Page IDs.
        chunks_with_ids = calculate_chunk_ids(chunks)

        # Add or Update the documents.
        existing_items = db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        logger.info(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            logger.info(f"Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
        else:
            logger.info("No new documents to add")
    except Exception as e:
        logger.error(f"Error adding documents to Chroma: {e}")
        raise


def calculate_chunk_ids(chunks: List[Document]) -> List[Document]:
    """
    Generates unique chunk IDs for each document chunk in the list.
    
    The IDs are formatted as follows:
    "data/{document_name}:page_number:chunk_index"
    
    Args:
        chunks (List[Document]): A list of Document objects representing the chunks to which IDs will be assigned.
            - Each Document object should contain information like its source file name and page number.
    
    Returns:
        List[Document]: A list of Document objects with updated IDs assigned to each chunk.
            - Each Document will now include an 'id' field or attribute with a unique chunk identifier.
    """
    try:
        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks

    except Exception as e:
        logger.error(f"Error calculating chunk IDs: {e}")
        return []


def clear_database() -> None:
    """
    Clears the existing Chroma database.
    
    Returns:
        None
    """
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
        else:
            logger.warning("Chroma database directory does not exist.")
    except Exception as e:
        logger.error(f"Error clearing the database: {e}")
        raise
