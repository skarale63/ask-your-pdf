import streamlit as st
import pandas as pd
from io import StringIO
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain



def user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        if i%2 == 0:
            st.write("User: ", message.content)
        else:
            st.write("Reply: ", message.content)
    return user_question, message.content


def main():
    st.set_page_config("gen_ai_project")
    st.header("Ask Your PDF")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if "qa_pairs" not in st.session_state:
        st.session_state.qa_pairs = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    if user_question:
        question, answer = user_input(user_question)
        st.session_state.qa_pairs.append({"Question": question, "Answer": answer})


    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.success("Done")

        # Generate CSV button
        st.info("Click the button below to generate a CSV of your questions and answers.")
        if st.button("Generate CSV"):
            with st.spinner("Processing..."):
                df = pd.DataFrame(st.session_state.qa_pairs)
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                st.session_state.generated_csv = csv_buffer.getvalue()
                st.success("CSV generated!")
        
        # Download button
        if "generated_csv" in st.session_state:
            st.download_button(
                label="Download CSV",
                data=st.session_state.generated_csv,
                file_name="qa_history.csv",
                mime="text/csv"
            )




if __name__ == "__main__":
    main()