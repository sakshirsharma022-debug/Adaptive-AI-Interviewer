from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_resume_and_jd(resume_text, jd_text):

    prompt = f"""
    You are an expert AI hiring assistant.

    Analyze the candidate's resume against the job description.

    Return:
    1. Match Score out of 100
    2. Top Strengths
    3. Missing Skills
    4. 5 Personalized Technical Interview Questions

    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def generate_interview_question(
        retrieved_context,
        conversation_history,
        difficulty,
        covered_topics,
        role_type
):
    stage_map = {
        "easy": "introductory",
        "medium":"fundamental",
        "hard":"advanced"
    }

    interview_stage = stage_map[difficulty]

    if len(conversation_history) == 0:
        interview_stage = "introductory"
    
    
    prompt = f"""

    You are an experienced and conversational AI technical interviewer.

    Your goal is to simulate a realistic technical interview experience.

    The interview should feel:
    - natural
    - adaptive
    - human
    - progressive
    - conversational

    You should NOT sound robotic or overly academic.

    --------------------------------------------------
    INTERVIEW CONTEXT
    --------------------------------------------------

    Current Difficulty Level:
    {difficulty}

    Current Interview Stage:
    {interview_stage}

    Retrieved Candidate Context:
    {retrieved_context}

    Previously Covered Topics:
    {covered_topics}

    Previous Conversation:
    {conversation_history}



    --------------------------------------------------
    INTERVIEW STAGE BEHAVIOR
    --------------------------------------------------

    If the interview stage is "introductory":

    - Focus on making the candidate comfortable.
    - Ask resume walkthrough questions.
    - Ask project discussion questions.
    - Ask implementation experience questions.
    - Ask reflective engineering questions.
    - Keep the tone warm and conversational.

    DO NOT:
    - ask deep theoretical questions
    - ask system design optimization questions
    - ask difficult architecture questions
    - ask multiple concepts at once

    GOOD introductory questions:
    - Can you walk me through the AI project you enjoyed building the most?
    - What inspired you to build this project?
    - Which part of the implementation was the hardest?
    - I noticed you worked with FastAPI — how was your experience building the backend?
    - What challenges did you face while integrating retrieval into your pipeline?

    BAD introductory questions:
    - Explain retrieval optimization.
    - Explain vector indexing tradeoffs.
    - Explain chunk overlap mathematically.
    - How would you optimize long-tail retrieval latency?

    --------------------------------------------------

    If the interview stage is "fundamental":

    - Focus on one concept at a time.
    - Test practical understanding instead of memorization.
    - Ask follow-up questions based on candidate experience.

    Focus more on the candidate's uploaded resume, projects, technologies, tools, and job description requirements.

    The interview should naturally adapt to the candidate's domain, experience level, and role expectations.

    Example domains may include:
    - AI/ML Engineering
    - Backend Development
    - Frontend Development
    - Product Management
    - Data Analytics
    - DevOps
    - Cloud Engineering

    Current Candidate Role Context:
    {role_type}

    GOOD fundamental questions:
    - Why did you choose FAISS for vector retrieval?
    - How does chunk overlap improve retrieval quality?
    - What role do embeddings play in semantic search?
    - What challenges did you face while building your API?

    --------------------------------------------------

    If the interview stage is "advanced":

    - Ask practical architecture and optimization questions.
    - Ask scenario-based engineering questions.
    - Explore scaling and tradeoffs.
    
    Focus advanced questions around:
    - system design
    - scalability
    - architecture decisions
    - production challenges
    - optimization tradeoffs
    - real-world engineering decisions

    Adapt these topics naturally based on the candidate's domain and projects.
    

    GOOD advanced questions:
    - How would you reduce retrieval latency in a production RAG pipeline?
    - What tradeoffs would you consider while scaling this system?
    - How would you improve retrieval quality for noisy queries?
    - How would you design session persistence for large-scale interviews?

    --------------------------------------------------
    IMPORTANT RULES
    --------------------------------------------------
    - Avoid overly theatrical or assistant-like introductions.
    - Keep the conversation concise and natural like a real interviewer.
    - Avoid overly theatrical or assistant-like introductions.
    - Ask ONLY ONE question.
    - Avoid directly repeating previous questions, but it is acceptable to revisit related concepts from a different angle if needed to continue the interview naturally.    .
    - Questions should feel personalized to the candidate.
    - Questions should feel like a real interviewer is speaking.
    - Avoid overly long questions.
    - Avoid sounding robotic.
    - Never generate bullet points.
    - Never explain the question.
    - Return ONLY the interview question.

    Do not start questions with:
    - "Let's start our interview"
    - "I'm excited to"
    - "To confirm"
    - "Thank you for sharing"
    - "Great job"
    - Do not mention repeated phrases in the begining of the question.

    Avoid assistant-like phrasing.

    """


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
    

def evaluate_history(
        question,
        answer,
        conversation_history
):
    prompt = f"""
    You are a supportive AI interviewer helping a final-year AI/ML student prepare for internships.

    Your role is to:
    - evaluate answers realistically
    - encourage learning
    - recognize partially correct understanding
    - guide the candidate toward improvement
    - behave like a helpful mentor interviewer

    Previous Conversation:
    {conversation_history}

    Current Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate the answer using the following format:

    1. Technical Understanding
    - What did the candidate understand correctly?
    - Mention positive points first.

    2. Missing Concepts
    - What important concepts were missing?
    - Keep this concise and beginner-friendly.

    3. Improvement Suggestion
    - Suggest how the candidate could improve the answer.
    - Explain simply and practically.

    4. Communication Feedback
    - Briefly evaluate clarity and confidence.

    5. Follow-Up Question
    - Ask ONE short follow-up question.
    - Keep it internship-level.
    - Focus on helping the candidate improve understanding.

    6. Difficulty Recommendation
    - Return ONLY one of:
        easy
        medium
        hard

    Base this on:
    - technical understanding
    - confidence
    - communication clarity
    - consistency across conversation

    IMPORTANT RULES:
    - The candidate is a student, not a senior engineer.
    - Reward partially correct answers.
    - If the candidate says they don’t know the answer, appreciate honesty and encourage learning.
    - Avoid harsh language like:
    "red flag"
    "failure"
    "poor understanding"
    - Do NOT ask research-level or highly advanced system design questions.
    - Keep the tone conversational, encouraging, and realistic.
    - Keep feedback concise and natural.
    - Keep improvement suggestions practical and internship-level.w
    """
        
        
    response = client.chat.completions.create(
        model = "LLama-3.1-8b-instant",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content

def generate_final_feedback(
    conversation_history
):
    prompt = f"""

    You are an experienced AI technical interviewer.

    Your task is to generate a final interview performance report for the candidate based on the complete interview conversation history.

    Conversation History:
    {conversation_history}

    The report should sound professional, realistic, constructive, and encouraging.

    The feedback should feel like a real interviewer evaluating an AI/ML internship candidate.

    --------------------------------------------------
    IMPORTANT INSTRUCTIONS
    --------------------------------------------------

    - Be specific and personalized.
    - Mention the candidate's strengths clearly.
    - Mention weak areas honestly but constructively.
    - Focus on practical AI/ML engineering skills.
    - Evaluate both technical understanding and communication clarity.
    - Avoid robotic language.
    - Avoid generic motivational phrases.
    - Keep the tone concise and professional.
    - Do NOT use markdown tables.
    - Do NOT generate bullet points with symbols like *, -, or •.
    - Keep formatting clean and UI-friendly.

    --------------------------------------------------
    RETURN RESPONSE IN THIS EXACT FORMAT
    --------------------------------------------------

    Overall Score: X/10

    1. Technical Strengths:
    Write 3-5 lines about the candidate's strongest technical abilities, projects, engineering decisions, or AI understanding.

    2. Areas For Improvement:
    Write 3-5 lines about missing concepts, weak explanations, shallow understanding, or areas needing deeper learning.

    3. Communication Assessment:
    Evaluate how clearly and confidently the candidate explained concepts and projects.

    4. Interview Progression:
    Analyze whether the candidate improved throughout the interview, adapted to questions, or handled increasing difficulty well.

    5. Interview Readiness:
    Give a realistic assessment of whether the candidate appears ready for:
    - AI internships
    - beginner ML roles
    - production AI projects

    6. Recommended Next Steps:
    Suggest practical next learning steps, technologies, or improvements that would help the candidate grow further.

    --------------------------------------------------
    FINAL RULES
    --------------------------------------------------

    - Return ONLY the report.
    - Do NOT add introductions.
    - Do NOT add closing statements.
    - Keep the formatting consistent.
    - Keep section titles exactly as specified.

    """
    
    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content
