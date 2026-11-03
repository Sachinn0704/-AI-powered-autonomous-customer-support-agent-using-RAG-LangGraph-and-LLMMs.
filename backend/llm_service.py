import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def generate_answer(question, context):

    prompt = f"""
You are ResolveAI, a professional customer support assistant.

Answer the customer's question using only the supplied knowledge base context.

If the answer is not available in the context, clearly say that you do not have enough information.

Knowledge Base Context:
{context}

Customer Question:
{question}

Provide a clear, polite and concise answer.
"""

    try:
        response = httpx.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"]

    except httpx.RequestError as error:
        raise RuntimeError(
            f"LLM service unavailable: {error}"
        )

    except httpx.HTTPStatusError as error:
        raise RuntimeError(
            f"LLM request failed: {error}"
        )


if __name__ == "__main__":

    context = """
    Customers can request refunds within 30 days of delivery.
    Only delivered and paid orders are eligible.
    """

    question = "What is the refund period?"

    answer = generate_answer(question, context)

    print("\nResolveAI Answer:")
    print(answer)
