import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()  # read the API key from .env

# The Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0.3)

# A reusable prompt with two blanks to fill in
prompt = PromptTemplate.from_template(
    "You are a data scientist. Context:\n{context}\n\nQuestion:\n{question}"
)

# Chain: fill the prompt -> send to Gemini -> return plain text
chain = prompt | llm | StrOutputParser()


def ask_ai(question, context, step):
    answer = chain.invoke({"context": context, "question": question})

    # Save the exchange so it can go in the report's AI log
    entry = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "step": step,
        "context": context,
        "question": question,
        "ai_response": answer,
        "decision": "",
        "justification": "",
    }
    
    log = []
    if os.path.exists("report/ai_log.json"):
        with open("report/ai_log.json", "r", encoding="utf-8") as f:
            log = json.load(f)
    log.append(entry)
    with open("report/ai_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

    return answer