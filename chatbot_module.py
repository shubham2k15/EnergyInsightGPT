import streamlit as st

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from llm_provider import get_llm


# ---------------- VECTOR STORE (SESSION BASED) ----------------
def get_vectorstore():
    # ✅ Reuse if already created
    if "vectorstore" in st.session_state and st.session_state["vectorstore"] is not None:
        return st.session_state["vectorstore"]

    # 🔥 IMPORTANT: get ONLY session docs (not folder)
    docs = st.session_state.get("docs", [])

    if not docs:
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    st.session_state["vectorstore"] = vectorstore

    return vectorstore


# ---------------- CLEAN OUTPUT ----------------
def clean_output(text):
    lines = text.split("\n")
    bullets = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if any(x in line.lower() for x in ["context", "question", "answer"]):
            continue

        if len(line.split()) < 4:
            continue

        if not line.startswith(("-", "*", "•")):
            bullets.append(f"- {line}")
        else:
            bullets.append(line)

    return "\n".join(bullets[:5]) if bullets else "- Unable to generate clear answer"


# ---------------- POLICY DETECTION ----------------
def is_policy_query(query):
    keywords = [
        "policy", "tax", "esg", "government", "regulation",
        "law", "compliance", "carbon credit", "subsidy",
        "incentive", "framework", "standard", "certificate",
        "emission rule"
    ]

    query_lower = query.lower()

    if any(k in query_lower for k in keywords):
        return True

    llm = get_llm()
    try:
        result = llm.invoke(f"""
Is this question related to sustainability policies, regulations, or government rules?

Answer ONLY YES or NO.

Question: {query}
""").content.strip().upper()

        return "YES" in result
    except:
        return False


# ---------------- BASIC ANSWER ----------------
def basic_answer(query):
    llm = get_llm()

    if is_policy_query(query):
        prompt = f"""
You are a GLOBAL sustainability policy expert.

- Answer exactly what is asked
- Cover all topics clearly
- Avoid unnecessary examples

Question:
{query}

Return:
- Structured bullet points
"""
    else:
        prompt = f"""
You are a sustainability expert.

- Give practical, real-world advice
- Be specific
- No generic answers

Question:
{query}

Return:
- Bullet points
"""

    response = llm.invoke(prompt).content

    return clean_output(response)


# ---------------- MAIN FUNCTION (RAG) ----------------
def answer_question(query):
    try:
        if not st.session_state.get("has_data", False):
            return "⚠️ Upload data first."

        vectorstore = get_vectorstore()

        if vectorstore is None:
            return "⚠️ No documents available."

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(query)

        if not docs:
            return "⚠️ No relevant data found."

        # 🔥 DEBUG (optional)
        # st.write(docs)

        context = "\n".join([doc.page_content for doc in docs])[:1500]

        llm = get_llm()

        prompt = f"""
You are an expert energy analyst.

STRICT RULES:
- Use ONLY the provided context
- Do NOT assume anything
- If unsure, say "Not enough data"

Context:
{context}

Question:
{query}

Return:
- 3 to 5 bullet points
- Clear, data-backed insights
"""

        response = llm.invoke(prompt).content

        return clean_output(response)

    except Exception as e:
        return f"⚠️ Error: {str(e)}"