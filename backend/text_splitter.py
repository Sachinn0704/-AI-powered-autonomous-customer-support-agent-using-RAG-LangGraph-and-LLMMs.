from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import load_documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    print(f"Successfully created {len(chunks)} text chunks.")

    return chunks


if __name__ == "__main__":

    documents = load_documents()

    chunks = split_documents(documents)

    for index, chunk in enumerate(chunks, start=1):

        print(f"\nChunk {index}")
        print("Source:", chunk.metadata["source"])
        print("Content:", chunk.page_content)
