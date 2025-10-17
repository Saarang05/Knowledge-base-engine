import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Initialize client lazily to avoid import-time failures
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        _client = OpenAI(api_key=api_key)
    return _client

# Template for generating context-aware answers
PROMPT_TEMPLATE = """
You are a knowledgeable assistant. Use ONLY the following context to answer the user's question.
If the answer cannot be found in the context, respond exactly with: "I don’t know based on the provided documents."

Instructions:
- Answer succinctly in 3-6 sentences.
- Cite source filenames inline like [source: {{doc_id}}] when relevant.
- Do not fabricate or use external knowledge.

Context:
{context}

Question:
{question}

Answer:
"""

def synthesize_answer(question, context_chunks, model=None):
    """
    Given a user question and retrieved context chunks,
    synthesize a concise and accurate answer using an LLM.
    """
    # Join context chunks
    context = "\n\n".join(context_chunks) if context_chunks else ""

    # Fill in the prompt template
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    # Call the OpenAI API using the new interface
    try:
        client = get_client()
        use_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        response = client.chat.completions.create(
            model=use_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=400
        )

        # Return the generated answer
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Provide graceful degradation message
        return f"An error occurred while generating the answer: {e}"
