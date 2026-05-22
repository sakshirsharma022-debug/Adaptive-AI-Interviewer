# Adaptive AI Interviewer

An AI-powered interview practice platform designed to simulate realistic technical interviews using conversational AI and Retrieval-Augmented Generation (RAG).

The system analyzes resumes and job descriptions, generates personalized interview questions, adapts question difficulty based on candidate performance, and provides detailed feedback to help users improve their interview skills.

Unlike traditional chatbot-style interview systems, this project focuses heavily on conversational flow, adaptive behavior, contextual memory, and realistic interview progression.

---

## Features

* Resume + Job Description analysis
* Personalized AI-generated interview questions
* Retrieval-Augmented Generation (RAG) pipeline
* FAISS-based semantic vector search
* Adaptive difficulty progression
* Session-based conversational memory
* Topic tracking to avoid repetitive questions
* AI-powered answer evaluation
* Structured final performance reports
* Responsive conversational frontend UI
* FastAPI backend deployment

---

## Tech Stack

### Backend

* FastAPI
* Python
* Groq LLM API
* LangChain
* FAISS
* Sentence Transformers

### Frontend

* HTML
* CSS
* JavaScript

### Deployment

* Render
* Vercel

---

## How It Works

1. The user uploads a resume and a job description.
2. The system extracts and chunks relevant information.
3. Embeddings are generated and stored using FAISS vector search.
4. The AI interviewer generates personalized interview questions based on retrieved context.
5. Difficulty dynamically adapts based on candidate responses.
6. The platform evaluates answers, tracks conversation history, and generates detailed interview feedback.

---

## Key Engineering Decisions

### Why FAISS instead of Pinecone?

FAISS was chosen because the platform currently operates on relatively small, session-scoped datasets generated dynamically from uploaded resumes and job descriptions. Local vector retrieval allowed faster prototyping with lower infrastructure overhead.

### Why RAG?

RAG improves contextual grounding by retrieving relevant resume and JD information before question generation, helping reduce generic questioning and improving personalization.

### Why Adaptive Difficulty?

The interviewer dynamically adjusts question complexity based on previous answers to simulate a more realistic interview experience.

---

## Future Improvements

* Voice-based conversational interviews
* Real-time speech-to-text integration
* Persistent session storage using Redis
* Advanced reranking pipelines
* Multi-agent interviewer architecture
* Analytics dashboard for interview performance tracking

---

## Project Goal

The goal of this project was not just to build another chatbot, but to design a more realistic conversational AI interview experience that feels adaptive, contextual, and human-like.

