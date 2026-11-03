from pathlib import Path
from langchain_core.documents import Document

DOCUMENTS_PATH = Path(__file__).parent / "knowledge_base" / "documents"


def load_documents():

    documents = []

    for file_path in DOCUMENTS_PATH.glob("*.txt"):

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        if content.strip():
            document = Document(
                page_content=content,
                metadata={
                    "source": file_path.name
                }
            )

            documents.append(document)

    print(f"Successfully loaded {len(documents)} documents.")

    return documents


if __name__ == "__main__":

    loaded_documents = load_documents()

    for document in loaded_documents:
        print("\nDocument:", document.metadata["source"])
        print("Content length:", len(document.page_content))
