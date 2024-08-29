import streamlit as st
from document_processor import process_document
from comparison_engine import compare_documents

def main():
    st.title("Document Comparison App")

    # File uploaders
    doc1 = st.file_uploader("Upload first document", type=["pdf", "txt"])
    doc2 = st.file_uploader("Upload second document", type=["pdf", "txt"])

    # Prompt input
    comparison_prompt = st.text_area(
        "Enter comparison prompt",
        "Compare the following two document excerpts and provide a detailed analysis of their similarities and differences:"
    )

    if doc1 and doc2 and comparison_prompt:
        if st.button("Compare Documents"):
            with st.spinner("Processing documents..."):
                doc1_text = process_document(doc1)
                doc2_text = process_document(doc2)
                similarity, summary = compare_documents(doc1_text, doc2_text, comparison_prompt)
                st.subheader("Comparison Results")
                st.write(f"Similarity Score: {similarity:.2f}")
        
                st.subheader("Summary of Differences:")
                if summary == "No significant differences found between the documents.":
                    st.write(summary)
                else:
                    st.write(summary)
                
                st.subheader("Raw Text Comparison:")
                st.text_area("Document 1 (First 500 characters)", doc1_text[:500], height=200)
                st.text_area("Document 2 (First 500 characters)", doc2_text[:500], height=200)

if __name__ == "__main__":
    main()