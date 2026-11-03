# ResolveAI – AI-Powered Autonomous Customer Support Agent

An AI-powered customer support prototype that combines Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), LangGraph workflows, and FastAPI to automate customer support operations.

ResolveAI is designed to handle common ecommerce support requests, including order tracking, refund requests, cancellations, returns, and policy-related questions.

The system combines rule-based business logic with an LLM-powered knowledge assistant to provide structured and context-aware customer support.

---

## 1. Project Overview

Customer support teams frequently handle repetitive requests involving order status, refunds, returns, cancellations, and payment-related questions.

ResolveAI explores how artificial intelligence and workflow automation can simplify these operations.

The application provides:

* Customer support query handling.
* Order tracking through a simulated order API.
* Refund eligibility verification.
* Refund risk assessment.
* Human approval for high-risk refund requests.
* Order cancellation workflow.
* Return request registration.
* Knowledge-base document retrieval.
* Context-aware AI response generation using RAG and an LLM.

## 2. Problem Statement

Traditional customer support systems often depend on manual processes for handling repetitive customer queries.

This can result in:

* Delayed responses.
* Repetitive manual work.
* Inconsistent policy information.
* Difficulty managing refund requests.
* Limited automation of routine support operations.

## 3. Proposed Solution

ResolveAI provides a prototype customer support automation system that combines backend APIs, business rules, AI-based knowledge retrieval, and language model integration.

The system uses:

1. FastAPI for backend services.
2. SQLite and SQLAlchemy for data management.
3. LangGraph for structured refund workflow orchestration.
4. Sentence Transformers for text embeddings.
5. ChromaDB for vector storage and similarity search.
6. Retrieval-Augmented Generation for knowledge retrieval.
7. Ollama with Qwen 2.5 3B for local language model inference.
8. HTML, CSS, and JavaScript for the frontend.

---

## 4. System Architecture

```text
                   CUSTOMER
                      |
                      v
              FRONTEND INTERFACE
              HTML / CSS / JavaScript
                      |
                      v
                 FASTAPI SERVER
                  Port: 8000
                      |
          +-----------+------------+
          |           |            |
          v           v            v
      SUPPORT       REFUND       AI CHAT
       AGENT        WORKFLOW       API
          |           |            |
          |           v            v
          |        LANGGRAPH      RAG PIPELINE
          |           |            |
          |           v            v
          |      BUSINESS RULES  CHROMADB
          |           |            |
          |           v            v
          |      RISK CHECK    SENTENCE TRANSFORMERS
          |           |            |
          |           v            v
          |      HUMAN REVIEW   RETRIEVED CONTEXT
          |                        |
          |                        v
          |                    OLLAMA
          |                        |
          |                        v
          |                   QWEN 2.5 3B
          |                        |
          +------------+-----------+
                       |
                       v
                CUSTOMER RESPONSE
```

### External Mock Order Service

A separate FastAPI application simulates an ecommerce order service.

```text
             MAIN FASTAPI APPLICATION
                       |
                       v
               HTTPX HTTP REQUEST
                       |
                       v
                MOCK ORDER API
                   Port 8001
                       |
                       v
                ORDER INFORMATION
```

The mock API provides simulated order information and cancellation operations.

---

## 5. Technology Stack

### Programming Languages

* Python
* JavaScript
* HTML5
* CSS3
* SQL

### Backend Frameworks

* FastAPI – REST API development.
* Uvicorn – ASGI application server.
* SQLAlchemy – Object Relational Mapper.
* Pydantic – Request validation through FastAPI schemas.

### Artificial Intelligence and LLM

* Ollama – Local LLM execution.
* Qwen 2.5 3B – Language model.
* LangGraph – Workflow orchestration.
* LangChain – Components for document processing and vector retrieval.
* Sentence Transformers – Text embedding generation.
* all-MiniLM-L6-v2 – Embedding model.

### RAG and Vector Database

* ChromaDB – Vector storage and similarity search.
* LangChain Community – Vector database integration.
* LangChain Text Splitters – Document chunking.
* LangChain Core – Embedding interface.

### Python Libraries

* HTTPX – HTTP communication.
* NumPy – Numerical operations.
* SQLAlchemy – Database operations.
* Sentence Transformers – Semantic embeddings.
* ChromaDB – Vector database.
* PyPDF – PDF document loading dependency.

### Database

* SQLite

### Frontend

* HTML
* CSS
* JavaScript

### Development Tools

* Visual Studio Code
* PowerShell
* Git
* GitHub
* Ollama

---

## 6. Core Features

### 6.1 Customer Support Agent

The support agent identifies customer intent and routes requests to the appropriate support workflow.

Supported intents include:

* Order tracking.
* Refund requests.
* Return requests.
* Order cancellation.
* Payment-related queries.
* Customer complaints.
* General support questions.

The current intent detection implementation uses rule-based keyword matching.

### 6.2 Order Tracking

Customers can provide an order number to retrieve order information.

Example:

```text
Customer: Where is my order ORD1001?

ResolveAI:
Order Number: ORD1001
Product: Wireless Headphones
Amount: ₹2500
Order Status: delivered
Payment Status: paid
```

Order information is retrieved from the simulated external order API.

### 6.3 Refund Processing

The refund workflow checks:

* Whether the order exists.
* Whether the order has been delivered.
* Whether payment has been completed.
* Whether the request falls within the 30-day refund period.
* Customer refund request history.
* Refund risk conditions.

Refund decisions are based on implemented business rules.

### 6.4 Fraud and Risk Assessment

The prototype includes basic risk assessment rules.

Examples of high-risk conditions:

* Three or more previous refund requests.
* Refund amount greater than ₹10,000.

High-risk requests are escalated for human review.

These are prototype rules, not a trained fraud detection model.

### 6.5 Human-in-the-Loop Approval

High-risk refund requests can be reviewed by a human through the refund review API.

The system supports approval or rejection of pending review requests.

### 6.6 Order Cancellation

The cancellation workflow communicates with the mock order API.

The simulated cancellation service supports cancellation of orders that are in processing status.

### 6.7 Return Management

The application checks basic return eligibility and records return requests in SQLite.

The current prototype does not arrange actual product pickups or logistics.

---

## 7. Retrieval-Augmented Generation (RAG)

ResolveAI implements a RAG pipeline to retrieve relevant information from customer support policy documents before generating AI responses.

### RAG Architecture

```text
           KNOWLEDGE BASE DOCUMENTS
                      |
                      v
                DOCUMENT LOADER
                      |
                      v
                 TEXT SPLITTER
                      |
                      v
              DOCUMENT CHUNKS
                      |
                      v
           SENTENCE TRANSFORMERS
             all-MiniLM-L6-v2
                      |
                      v
                EMBEDDINGS
                      |
                      v
                 CHROMADB
                      |
                      |
              CUSTOMER QUESTION
                      |
                      v
              QUERY EMBEDDING
                      |
                      v
              SIMILARITY SEARCH
                      |
                      v
              RETRIEVED CONTEXT
                      |
                      v
                 OLLAMA LLM
                      |
                      v
              GENERATED RESPONSE
```

### Knowledge Base Documents

The project contains the following policy documents:

* refund_policy.txt
* return_policy.txt
* cancellation_policy.txt
* faq.txt

### Document Processing

The RAG pipeline performs:

1. Loading policy documents.
2. Splitting documents into smaller chunks.
3. Generating semantic embeddings.
4. Storing embeddings in ChromaDB.
5. Retrieving relevant chunks using similarity search.
6. Supplying retrieved context to the language model.

### Embedding Model

Model: `all-MiniLM-L6-v2`

The embedding model produces 384-dimensional vectors.

### Vector Database

ChromaDB stores the document embeddings and supports semantic similarity search.

---

## 8. Large Language Model Integration

ResolveAI uses Ollama to run a local language model.

### Model Details

* Runtime: Ollama
* Model: Qwen 2.5 3B
* API: Ollama Generate API
* Endpoint: `http://localhost:11434/api/generate`

### LLM Workflow

1. Customer submits a question.
2. RAG retrieves relevant policy information.
3. Retrieved context is supplied to the LLM.
4. Qwen generates a natural-language response.
5. The response and source filenames are returned to the frontend.

The language model is instructed to answer using the supplied knowledge-base context and acknowledge when sufficient information is unavailable.

---

## 9. LangGraph Refund Workflow

The refund processing module uses LangGraph to organize the refund decision process.

### Workflow

```text
             CUSTOMER REFUND REQUEST
                       |
                       v
                  ORDER LOOKUP
                       |
                       v
                  POLICY CHECK
                       |
                       v
                CUSTOMER HISTORY
                       |
                       v
                   FRAUD CHECK
                       |
                       v
                  DECISION NODE
                       |
           +-----------+-----------+
           |           |           |
           v           v           v
        APPROVED     REJECTED   HUMAN REVIEW
           |           |           |
           +-----------+-----------+
                       |
                       v
                FINAL RESPONSE
```

The workflow uses structured state transitions and deterministic business rules.

LangGraph currently orchestrates the refund workflow; the complete support system is not yet a fully autonomous multi-agent system.

---

## 10. Database Design

Database: SQLite

ORM: SQLAlchemy

The backend contains database models for:

* Customers
* Orders
* Refund Requests
* Investigation Logs
* Return Requests

### Database Operations

The application supports:

* Customer verification.
* Refund request storage.
* Refund status tracking.
* Investigation log storage.
* Human review status updates.
* Return request registration.

---

## 11. Backend API Endpoints

### Main FastAPI Application

Base URL:

`http://127.0.0.1:8000`

| Method | Endpoint                      | Purpose                      |
| ------ | ----------------------------- | ---------------------------- |
| GET    | `/`                           | Backend health/root response |
| POST   | `/chat`                       | Customer support interaction |
| POST   | `/refunds`                    | Submit refund request        |
| GET    | `/refunds`                    | Retrieve refund requests     |
| GET    | `/refunds/{refund_id}/logs`   | Retrieve investigation logs  |
| POST   | `/refunds/{refund_id}/review` | Human refund review          |
| POST   | `/knowledge`                  | Knowledge-base retrieval     |
| POST   | `/ai-chat`                    | RAG-powered AI response      |

API documentation:

`http://127.0.0.1:8000/docs`

### Mock Order API

Base URL:

`http://127.0.0.1:8001`

| Method | Endpoint                        | Purpose                     |
| ------ | ------------------------------- | --------------------------- |
| GET    | `/`                             | Service root                |
| GET    | `/orders`                       | Retrieve simulated orders   |
| GET    | `/orders/{order_number}`        | Retrieve individual order   |
| POST   | `/orders/{order_number}/cancel` | Simulate order cancellation |

These endpoints belong to a local prototype service, not a real ecommerce platform.

---

## 12. Project Structure

```text
ResolveAI/
│
├── backend/
│   │
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── init_db.py
│   ├── seed_data.py
│   │
│   ├── tools.py
│   ├── agent.py
│   ├── support_agent.py
│   ├── mock_order_api.py
│   │
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_database.py
│   ├── rag_pipeline.py
│   ├── llm_service.py
│   ├── ai_rag_agent.py
│   │
│   ├── knowledge_base/
│   │   ├── documents/
│   │   │   ├── refund_policy.txt
│   │   │   ├── return_policy.txt
│   │   │   ├── cancellation_policy.txt
│   │   │   └── faq.txt
│   │   │
│   │   └── vector_store/
│   │
│   └── tests/
│
├── frontend/
│   │
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   │
│   ├── chat.html
│   ├── chat.css
│   ├── chat.js
│   │
│   ├── ai-chat.html
│   ├── ai-chat.css
│   └── ai-chat.js
│
├── .gitignore
├── README.md
└── requirements.txt
```

Note: The structure illustrates the intended organization of the project. Some testing files may remain directly inside the backend directory rather than inside a separate tests folder.

---

## 13. Installation and Setup

### Prerequisites

Install:

* Python 3.11
* Git
* Ollama
* Qwen 2.5 3B model

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ResolveAI
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Install and Run Ollama

Install Ollama from:

https://ollama.com/

Download the model:

```bash
ollama pull qwen2.5:3b
```

Run the model:

```bash
ollama run qwen2.5:3b
```

### Step 6: Initialize the Database

Open another terminal:

```powershell
cd backend
python init_db.py
```

If the project requires sample customer and order data:

```powershell
python seed_data.py
```

### Step 7: Build the Vector Database

From the backend directory:

```powershell
python vector_database.py
```

This processes the policy documents and stores their embeddings in ChromaDB.

### Step 8: Start the Mock Order API

```powershell
python -m uvicorn mock_order_api:app --reload --port 8001
```

### Step 9: Start the Main Backend

Open another terminal, activate the same virtual environment, and run:

```powershell
cd backend
python -m uvicorn main:app --reload --port 8000
```

### Step 10: Open the Frontend

Open the frontend files in a browser.

AI Chat:

```text
frontend/ai-chat.html
```

Main application:

```text
frontend/index.html
```

---

## 14. Current Project Limitations

ResolveAI is an academic and portfolio prototype.

The following limitations are important:

1. The order service uses simulated in-memory order data.
2. Order cancellation changes are not persistent after restarting the mock API.
3. Refund processing does not connect to a real payment gateway.
4. Refund risk assessment uses basic business rules rather than a trained fraud detection model.
5. Return requests are recorded but actual pickup and fulfilment are not implemented.
6. Intent detection currently uses rule-based keyword matching.
7. The AI knowledge assistant uses the local Ollama model and requires the model service to be available.
8. Customer authentication and production-grade authorization are not implemented.
9. The system has not been deployed as a production service.
10. The current AI chat does not independently execute all operational workflows.

---

## 15. Future Enhancements

The following are potential future improvements and are not claimed as completed features.

* Advanced LangGraph agent orchestration.
* Dynamic tool selection.
* Multi-turn conversation memory.
* Persistent conversation history.
* Customer authentication and authorization.
* Admin dashboard.
* Advanced refund and return analytics.
* More comprehensive automated testing.
* Improved observability and error handling.
* Docker containerization.
* Cloud deployment.
* Integration with real ecommerce APIs.
* Real payment gateway integration.
* Advanced fraud detection using machine learning.

---

## 16. Learning Outcomes

Through this project, the following concepts and technologies were explored:

* REST API development using FastAPI.
* Database management using SQLite and SQLAlchemy.
* Workflow orchestration using LangGraph.
* Rule-based decision systems.
* Retrieval-Augmented Generation.
* Document loading and text chunking.
* Semantic embeddings.
* Vector database operations.
* Similarity search.
* Local LLM inference using Ollama.
* Prompt engineering.
* Frontend-to-backend integration.
* HTTP communication between services.
* Git and GitHub project management.

---

## 17. Project Status

**Project:** ResolveAI

**Category:** Artificial Intelligence / Generative AI / Customer Support Automation

**Development Status:** Prototype implementation completed at the current development stage.

**Primary Focus:** RAG-based knowledge assistance, local LLM integration, customer support automation, and structured refund workflow orchestration.

---

## 18. Author

**Sachin B**

B.Tech – Data Science

GitHub: https://github.com/Sachinn0704

---

## 19. Disclaimer

ResolveAI is an educational and portfolio project developed to demonstrate the integration of AI, backend development, retrieval systems, and workflow automation.

It is not a production-ready customer support platform. All ecommerce operations and policies are simulated for demonstration and learning purposes.
