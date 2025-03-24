from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
def compare_documents(doc1_text, doc2_text, comparison_prompt):
    # Split texts into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    doc1_chunks = text_splitter.split_text(doc1_text)
    doc2_chunks = text_splitter.split_text(doc2_text)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(min_df=1, max_df=0.95, ngram_range=(1, 2))
    all_chunks = doc1_chunks + doc2_chunks
    tfidf_matrix = vectorizer.fit_transform(all_chunks)

    # Compare documents
    similarity_scores = []
    different_chunks = []

    for i, chunk in enumerate(doc1_chunks):
        chunk_vector = tfidf_matrix[i]
        similarities = cosine_similarity(chunk_vector, tfidf_matrix[len(doc1_chunks):])
        most_similar_index = similarities.argmax()
        score = similarities[0, most_similar_index]
        similarity_scores.append(score)
        
        if score < 0.90:  # Adjust this threshold as needed
            different_chunks.append((i, chunk, doc2_chunks[most_similar_index]))

    overall_similarity = sum(similarity_scores) / len(similarity_scores)

    # Generate detailed comparison using OpenAI GPT-4
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))
    prompt = ChatPromptTemplate.from_template(comparison_prompt + "\n\nDocument 1: {doc1}\n\nDocument 2: {doc2}")
    chain = LLMChain(llm=llm, prompt=prompt)

    detailed_comparisons = []
    for i, chunk1, chunk2 in different_chunks[:5]:
        try:
            result = chain.run(doc1=chunk1, doc2=chunk2, different_chunks=different_chunks)
            detailed_comparisons.append(f"Comparison of chunk {i}:\n{result}\n")
        except Exception as e:
            logging.error(f"Error generating comparison for chunk {i}: {str(e)}")
            detailed_comparisons.append(f"Comparison of chunk {i}: Error occurred during comparison.\n")

    if not detailed_comparisons:
        summary = "No significant differences found between the documents."
    else:
        summary = f"Found {len(different_chunks)} different chunks between the documents.\n\n"
        summary += "Detailed comparison:\n" + "\n".join(detailed_comparisons)

    return overall_similarity, summary