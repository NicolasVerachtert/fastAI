# FastAPI RAG-Based Chatbot API

This project provides a **FastAPI-based API** that delivers responses using a Retrieval-Augmented Generation (RAG) system powered by Large Language Models (LLMs). The system combines document-based context and conversational history to deliver highly relevant responses.

---

## Endpoints

- POST **`/chatbot`**: Accepts a query and returns a response from the LLM enriched with relevant document context and session history.
  - LLMQueryDto:
    ```json
    {
    "session_id": "string (uuid)",
    "question": "string",
    "language": "string (allowed: 'nederlands', 'english')",
    "game_mode": "string (allowed: 'classic', 'belgium')"
    }
    ```
- POST **`/prediction`**: Accepts the features from a boardgame and returns a prediction on popularity_score, average_rating, average_complexity
  - BoardGameDto:
    ```json
    {
     "year_published": "int",
     "min_players": "int",
     "max_players": "int",
     "play_time": "int",
     "min_age": "int",
     "mechanics": "list[str]",
     "domains": "list[str]"
    }
    ```
- GET **`/prediction/available-mechanic`**: Returns a list[str] which defines the available and accepted mechanics of the boardgame for the model
- GET **`/prediction/available-domain`**: Returns a list[str] which defines the available and accepted domains of the boardgame for the model
- **Standard FastAPI Endpoints**:
    - `/docs`: Swagger UI for interactive API exploration.
    - `/redoc`: API documentation in ReDoc format.
    - `/health`: A simple health check endpoint.

---

## Retrieval-Augmented Generation (RAG) System
### RAG App
#### Features
- **Vector Database**:
    - Uses **Chroma** to store vectorized document chunks.
    - Saves the vector database as an `.sqlite` file for persistence.
- **Document Management**:
    - Documents are uploaded to a Google Cloud Storage bucket using the format:
      ```
      'name'_'game mode'_'language'.'extension;
      ```
    - Supported game modes: `classic`, `belgium`.
    - Supported languages: `en`, `nl`.
    - Supported formats/extensions: `.txt`, `.md`, `.pdf`.
    - On container startup, documents are automatically pulled from the bucket and processed.
- **Embeddings**:
    - Embeddings are generated using **Google Generative AI Embeddings** and stored in the Chroma database.
- **Context Filtering**:
    - RAG searches the ChromaDB for the **top 5 contexts**, filtered by the relevant language and game mode.

#### Large Language Model (LLM) Integration
The application's LLM integration is powered by the **Langchain** package, which provides a flexible and extensible framework for working with large language models. 
Langchain allows seamless interaction with multiple LLMs, including **Gemini** and **Mistral**, and enables advanced functionality such as chaining models and integrating them with other services like embeddings and retrieval-augmented generation (RAG).
- **Primary Model**: **Gemini LLM**.
- **Fallback Model**: **Mistral**.
- Responses are tailored to the **language** specified in the query object (`nl` or `en`).

#### Session Management
- Previous questions and answers in the same session are saved to an SQLite database using **SQLAlchemy**.
- For new queries, the system includes prior session history as additional context alongside the RAG results.

#### Logging
- Logs are written to `app.log`:
    - Includes FastAPI application logs and query logs for debugging and monitoring.

### Model Customization

Currently, the application uses **Gemini** and **Mistral** as the primary LLMs. However, the system is designed to be easily extendable, and you can add additional models as follows:

1. **Extend the model**: To add a new LLM, create a new object by extending the `BaseChatModel` class from Langchain. See [Langchain chat models](https://python.langchain.com/docs/integrations/chat/).

2. **Register the new model**: In the `model_registry.py` file located in `service/rag/models`, you can register the new model. Use the `register_model()` function, specifying the model's priority and the new model object.

### API Key Management for Models

If the new model requires API keys, it is recommended to securely manage them using **Google Cloud Secret Manager**. Here’s how you can configure it:

1. **Store API Keys**: Add the model's API keys to **Google Cloud Secret Manager**.
2. **Configure Key ID**: Declare the key names in the **`config/environment.py`** file. For example:
   `LLM_KEY_ID = os.getenv("LLM_KEY_ID", "LLM_API_KEY")`
3. **Import in Secret Manager**: In the `config/secret_manager.py` file, ensure that the appropriate API key ID is imported, and the secret is fetched securely using the Google Cloud Secret Manager API.

This setup allows you to extend the system with additional models while ensuring that sensitive information (such as API keys) is stored securely and retrieved dynamically.

---

## Prediction Model

### Features

- A separate model has been trained for every feature that has to be predicted.
- The training and accompanying research can be found in /research.

---

## Environment Configuration

### Required Environment Variables
The following variables should be set for the application to run:
- **`CREDENTIALS_JSON`**: Path to the Google Cloud service account credentials file.

### Google Cloud Secret Manager
The application will retrieve the API keys for **Mistral** and **Gemini** from **Google Cloud Secret Manager**. You must ensure that the API keys are stored in Secret Manager under the following secret names:

- **`MISTRAL_API_KEY`**: The secret name in Google Cloud Secret Manager for the Mistral LLM API key.
- **`GEMINI_API_KEY`**: The secret name in Google Cloud Secret Manager for the Gemini LLM API key.

The application will automatically fetch these keys from Secret Manager using the names specified above when running.
By default, the application expects these specific secret names. However, if you wish to use different names for the secrets in Google Cloud Secret Manager, you can do so. 
In that case, you must provide the new secret name as an environment variable:

- **`MISTRAL_KEY_ID`**: The name of the secret in Google Cloud Secret Manager for the Mistral API key, if it differs from the default `MISTRAL_API_KEY`.
- **`GEMINI_KEY_ID`**: The name of the secret in Google Cloud Secret Manager for the Gemini API key, if it differs from the default `GEMINI_API_KEY`.

### Google Cloud Storage Bucket

The Google Cloud Storage (GCS) bucket and document path configurations are set in the `.env` file:

- **`GCS_BUCKET_NAME`**: The name of the GCS bucket where the documents are stored. The default value is:
  ```plaintext
  team-20-monopoly-ip2-media-bucket
  ```
- **`GCS_DOCS_PATH`**: The specific path within the GCS bucket where the documents are located. The default value is:
  ```plaintext
  monopoly-user-guides
  ```

### Optional Configuration via Environment Variables

The application allows further customization through additional environment variables. These variables are optional and can be configured to suit your specific use case:

- **`DATA_FOLDER`**: Path to the data directory. Default is `data`.
- **`UVICORN_PORT`**: The port number for the Uvicorn server. Default is `5000`.
- **`UVICORN_HOST`**: The host address for the Uvicorn server. Default is `0.0.0.0`.
- **`CHROMA_RESET`**: Whether to reset the Chroma database on startup. Default is `false`.
- **`ARTIFACTS_PATH`**: Path to the artifacts directory. Default is `artifacts`.
- **`PREDICTION_ARTIFACTS_PATH`**: Path to the prediction model artifacts. Default is `{ARTIFACTS_PATH}/prediction_model`.


### Google Cloud Configuration

- **`GOOGLE_PROJECT_ID`**: The Google Cloud project ID. Default is `integratieproject-2-442110`.
- **`GOOGLE_SERVICE_ACCOUNT_CRED_PATH`**: Path to the service account credentials file (`credentials.json`). Default is `credentials.json`.
- **`GCS_BUCKET_NAME`**: The name of the Google Cloud Storage bucket. Default is `team-20-monopoly-ip2-media-bucket`.
- **`GCS_DOCS_PATH`**: The path to the documents within the GCS bucket. Default is `monopoly-user-guides`.

### AI Model Configuration

- **Gemini AI**:
    - **`GEMINI_EMBEDDING_MODEL`**: The model used for embedding generation in Gemini. Default is `models/embedding-001`.
    - **`GEMINI_LLM_MODEL`**: The model used for generating responses with Gemini. Default is `gemini-1.5-flash-latest`.
    - **`GEMINI_KEY_ID`**: The ID of the secret in Google Cloud Secret Manager for the Gemini API key. Default is `GEMINI_API_KEY`.

- **Mistral AI**:
    - **`MISTRAL_KEY_ID`**: The ID of the secret in Google Cloud Secret Manager for the Mistral API key. Default is `MISTRAL_API_KEY`.
    - **`MISTRAL_LLM_MODEL`**: The model used for generating responses with Mistral. Default is `open-mistral-7b`.

These configuration options provide flexibility to customize paths, server settings, Google Cloud integration, and AI models according to your needs.

---

## Deployment

### Dockerized Application
- The project is compiled into a Docker image for seamless deployment.
- On container startup:
    1. Documents are pulled from the Google Cloud Storage bucket.
    2. Embeddings are generated and stored in the ChromaDB.
    3. The FastAPI application is started using **Uvicorn**, an ASGI server, to serve API requests.

---

## Usage Instructions

1. **Set Environment Variables**:
   Ensure the required environment variables are set before running the container.

2. **Run the Docker Container**:
   Start the container to initialize the application and load documents.

3. **Use the RESTful API**:
    - Send requests to the API endpoints.

---

## Limitations and Future Improvements

### Language Support
Currently, no additional languages are planned beyond **Dutch (nl)** and **English (en)**. The fallback mechanism uses the standard LLM parser when no relevant context is found in the vector database. However, please note that this fallback may result in reduced performance, as the embeddings are language-sensitive and are specifically generated for supported languages.

---

## Contributing

Please open issues or submit pull requests to contribute to this project. For questions or improvements, reach out to the repository maintainers.

---