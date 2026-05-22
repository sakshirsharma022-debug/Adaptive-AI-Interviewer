from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from parser import extracted_text_from_pdf
from llm_engine import analyze_resume_and_jd
from chunking import chunk_text
from embedding import create_vector_store, retrieve_relevant_context
from llm_engine import generate_interview_question, evaluate_history, generate_final_feedback
import uuid

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sessions = {}


@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/analyze")
async def analyze_file(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    try:

    
        resume_text = extracted_text_from_pdf(resume)
        jd_text = extracted_text_from_pdf(jd)

        


        analysis = analyze_resume_and_jd(
            resume_text,
            jd_text
        )
        

        resume_chunks = chunk_text(resume_text)
        jd_chunks = chunk_text(jd_text)
        
        all_chunks = resume_chunks + jd_chunks
        vector_store = create_vector_store(all_chunks)
        session_id = str(uuid.uuid4())

        sessions[session_id] = {

            "conversation_history": [],

            "difficulty": "easy",

            "vector_store": vector_store,

            "jd_text": jd_text,

            "covered_topics":[],

            "role":jd_text[:300]

        }
        query = "What are the candidate's strengths in AI and RAG?"

        context = retrieve_relevant_context(
            vector_store,
            query
        )

        return {
            
            "session_id": session_id,
            "retrieved_context":context,
            "analysis" : analysis
        }
    except Exception as e:
        return{
            "error": str(e)
        }
    
@app.post("/generate_question")
async def generate_question(
    data: dict = Body(...)
):
    try:

        session_id = data["session_id"]

        if session_id not in sessions:

            return{
                "error": "Invalid or expired session"
            }

        conversation_history = sessions[session_id]["conversation_history"]

        recent_history = conversation_history[-4:]

        difficulty = sessions[session_id]["difficulty"]

        vector_store = sessions[session_id]["vector_store"]

        jd_text = sessions[session_id]["jd_text"]

        covered_topics = sessions[session_id]["covered_topics"]

        role_type = sessions[session_id]["role_type"]

        query = f""" Important candidate skills and project experience relevant to:
        {
            jd_text[:300]
        }"""
        

        context = retrieve_relevant_context(
            vector_store,
            query

        )

        question = generate_interview_question(
            context,
            recent_history,
            difficulty,
            covered_topics,
            role_type
        )

        return{
            "question": question
        }
    except Exception as e:
        return{
            "error": str(e)
        }



@app.post("/evaluate_history")
async def evaluate_candidate_answer(
    data: dict = Body(...)

):
    
    try:

        session_id = data["session_id"]
        if session_id not in sessions:

            return{
                "error": "Invalid or expired session"
            }
        conversation_history = sessions[session_id]["conversation_history"]
        evaluation = evaluate_history(
            data["question"],
            data["answer"],
            conversation_history
        )

        evaluation_lower = evaluation.lower()

        difficulty_section  = evaluation_lower.split(
            "difficulty recommendation"
        )[-1][:50]

        if "hard" in difficulty_section:
            sessions[session_id]["difficulty"] = "hard"

        elif "medium" in difficulty_section:
            sessions[session_id]["difficulty"] = "medium"

        else:
            sessions[session_id]["difficulty"] = "easy"

        conversation_history.append({
            "question": data["question"],
            "answer": data["answer"],
            "evaluation": evaluation


        })

        sessions[session_id]["covered_topics"].append(data["question"])

        return {
            "evaluation": evaluation,
            "conversation_history": conversation_history
        }

    except Exception as e:

        return{
            "error": str(e)
        }

@app.post("/final_feedback")
async def final_feedback(
    data: dict = Body(...)

):
    try:

        session_id = data["session_id"]
        if session_id not in sessions:

            return{
                "error": "Invalid or expired session"
            }
        conversation_history = sessions[session_id]["conversation_history"]
        feedback = generate_final_feedback(
            conversation_history
        )

        return {
            "final_feedback": feedback
        }
    
    except Exception as e:
        return{
            "error": str(e)
        }