from vector_database import search_knowledge_base


def retrieve_context(question, k=3):

    results = search_knowledge_base(question, k=k)

    if not results:
        return {
            "success": False,
            "question": question,
            "answer": "I could not find relevant information in the knowledge base.",
            "sources": [],
            "context": ""
        }

    context_parts = []
    sources = []

    for document in results:

        context_parts.append(document.page_content)

        source = document.metadata.get("source", "Unknown")

        if source not in sources:
            sources.append(source)

    context = "\n\n".join(context_parts)

    answer = (
        "Here is the relevant information from our knowledge base:\n\n"
        + context
    )

    return {
        "success": True,
        "question": question,
        "answer": answer,
        "sources": sources,
        "context": context
    }


if __name__ == "__main__":

    question = input("Enter your customer question: ")

    result = retrieve_context(question)

    print("\nResolveAI RAG Response")
    print("----------------------")

    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print("-", source)
