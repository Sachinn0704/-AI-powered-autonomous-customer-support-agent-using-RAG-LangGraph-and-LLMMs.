from rag_pipeline import retrieve_context
from llm_service import generate_answer


def ask_ai(question):

    if not question.strip():
        return {
            "success": False,
            "reply": "Please enter a question.",
            "sources": []
        }

    try:
        result = retrieve_context(question, k=3)

        if not result["success"]:
            return {
                "success": False,
                "reply": result["answer"],
                "sources": []
            }

        answer = generate_answer(
            question=question,
            context=result["context"]
        )

        return {
            "success": True,
            "question": question,
            "reply": answer,
            "sources": result["sources"]
        }

    except RuntimeError as error:
        return {
            "success": False,
            "reply": "The AI service is temporarily unavailable.",
            "sources": [],
            "error": str(error)
        }


if __name__ == "__main__":

    print("ResolveAI - RAG + LLM Agent")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("Customer: ").strip()

        if question.lower() == "exit":
            break

        result = ask_ai(question)

        print("\nResolveAI:", result["reply"])

        if result["sources"]:
            print("Sources:", ", ".join(result["sources"]))

        print()
