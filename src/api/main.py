from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api.schemas import ChatRequest, ChatResponse
from src.agent.support_agent import SupportAgent
from src.generation.api_generator import APIGenerator
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent
    logger.info("Initializing SupportAgent... This may take a few seconds.")
    try:
        agent = SupportAgent(use_mock_generator=False)
        logger.info("SupportAgent initialized and ready.")
    except Exception as e:
        logger.error(f"Failed to initialize SupportAgent: {e}")
        agent = "FAILED"
    yield
    agent = None

app = FastAPI(
    title="TrustSupport API",
    description="Evidence-grounded and safety-aware gaming customer support agent.",
    version="1.1.0",
    lifespan=lifespan
)

# Allow CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None

@app.get("/health")
async def health_check():
    if agent is None:
        return {
            "status": "starting",
            "agent_loaded": False,
            "classifier_loaded": False,
            "retriever_loaded": False,
            "api_version": "1.1.0"
        }
    if agent == "FAILED":
        return {
            "status": "failed",
            "agent_loaded": False,
            "classifier_loaded": False,
            "retriever_loaded": False,
            "api_version": "1.1.0"
        }
        
    return {
        "status": "healthy",
        "agent_loaded": True,
        "classifier_loaded": hasattr(agent, 'classifier') and agent.classifier is not None,
        "retriever_loaded": hasattr(agent, 'retriever') and agent.retriever is not None,
        "api_version": "1.1.0"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.query or request.query.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"code": "EMPTY_QUERY", "message": "Please provide a support question."}
        )
        
    if agent is None:
        raise HTTPException(
            status_code=503, 
            detail={"code": "SERVICE_UNAVAILABLE", "message": "Agent is still initializing"}
        )
        
    if agent == "FAILED":
        raise HTTPException(
            status_code=500, 
            detail={"code": "INITIALIZATION_ERROR", "message": "The system failed to initialize properly."}
        )
        
    try:
        response_data = agent.respond(request.query)
        return ChatResponse(**response_data)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500, 
            detail={"code": "INTERNAL_ERROR", "message": "An unexpected error occurred while processing your request."}
        )
