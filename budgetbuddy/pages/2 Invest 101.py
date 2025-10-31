import streamlit as st
import os
from huggingface_hub import InferenceClient

# Set up Hugging Face API key
os.environ["HF_TOKEN"] = st.secrets["HF_TOKEN"]

# Initialize InferenceClient
client = InferenceClient(api_key=os.environ["HF_TOKEN"])

st.title('Getting started')
st.write(
    'Not sure how to begin investing? Look no further! This guide will walk you through the basics of investing, helping you make informed decisions to grow your wealth over time.'
)

tab1, tab2 = st.tabs(['Types of Investments', 'Resources to learn more'])

# Tab 1: Investment guide
with tab1:
    st.header('What should you consider?')
    st.write(
        'Different types of investments come with varying levels of risk and potential returns. It\'s essential to understand your risk tolerance before getting started.'
    )
    with st.expander('What is your risk appetite?', expanded=True):
        time = st.radio(
            'How long do you plan to invest for?',
            ['0 to 5 years', '5 to 10 years', '10+ years'],
            index=None,
        )
        if time == '0 to 5 years':
            option = 'Low'
        elif time == '5 to 10 years':
            option = 'Moderate'
        elif time == '10+ years':
            option = 'High' 
        else:
            option = 'Unknown'
    
        colour = {'Low':'green', 'Moderate':'orange', 'High':'red'}.get(option, 'white')
        st.write(
            'Your risk appetite is likely:', f"<p style='color:{colour}; font-size:25px; font-weight:800;'>{option}</span></b>", unsafe_allow_html=True
        )
        
    st.subheader('Investment Options')
    if option == 'Low':
        st.write('- Bonds, Cash')
    elif option == 'Moderate':
        st.write('- Bonds, Cash, Mutual Funds, ETFs')
    elif option == 'High':
        st.write('- Bonds, Cash, Mutual Funds, ETFs, Stocks')
    else:
        st.write('Please select an option to proceed.')

# Tab 2: Resources + Chatbot
with tab2:
    st.header('Want to learn more?')
    st.write(
        '- [Investopedia](https://www.investopedia.com/)\n'
        '- [SGX Academy](https://www.sgx.com/academy)\n'
        '- [MoneySense](https://www.moneysense.gov.sg/)'
    )

    st.subheader('Ask BudgetBuddy')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Ask BudgetBuddy anything"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Build full prompt for AI
        full_prompt = '\n'.join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

        # Get AI response from Falcon 7B model
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = client.text_generation(
                        model="tiiuae/falcon-7b-instruct",
                        inputs=full_prompt,
                        max_new_tokens=200
                    )
                    reply = result[0]["generated_text"].split("assistant:")[-1].strip()
                except Exception as e:
                    reply = f"Error generating response: {e}"

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
