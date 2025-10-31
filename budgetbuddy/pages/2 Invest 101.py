import streamlit as st
import os
from huggingface_hub import InferenceClient

# --- Streamlit Cloud / HF Token Setup ---
# The correct way to handle this in Streamlit Cloud is using st.secrets.
# We modify the initialization to be more robust for different environments.
try:
    # 1. Try to read from Streamlit secrets (Cloud environment)
    hf_token = st.secrets.get("HF_TOKEN")
except:
    # 2. Fallback to standard environment variable
    hf_token = os.environ.get("HF_TOKEN", None)

if not hf_token:
    # If token is still missing, display a warning placeholder instead of crashing the app
    st.warning("Hugging Face API Token (HF_TOKEN) not found. Chatbot functionality may be disabled. Please configure it in st.secrets.")

# Initialize InferenceClient
# The 'token' argument is the preferred way to pass the API key.
client = InferenceClient(token=hf_token)

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
    # Initialize 'time' and 'option' for display logic outside the radio widget
    time = None
    option = 'Unknown'
    
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
    
        colour = {'Low':'green', 'Moderate':'orange', 'High':'red'}.get(option, 'gray')
        st.write(
            'Your risk appetite is likely:', f"<p style='color:{colour}; font-size:25px; font-weight:800;'>{option}</span></b>", unsafe_allow_html=True
        )
        
    st.subheader('Investment Options')
    # Use the determined 'option' for investment recommendations
    if option == 'Low':
        st.write('- Bonds, Cash (Focus on preserving capital)')
    elif option == 'Moderate':
        st.write('- Bonds, Cash, Mutual Funds, ETFs (A balanced approach)')
    elif option == 'High':
        st.write('- Bonds, Cash, Mutual Funds, ETFs, Stocks (Potential for higher growth, but higher volatility)')
    else:
        st.write('Please select an investment horizon to see suggested options.')

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
        # Initialize conversation history
        st.session_state.messages = []

    # Display conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Ask BudgetBuddy anything"):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Build full prompt for AI by joining all previous messages
        full_prompt = '\n'.join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

        # Get AI response from Falcon 7B model
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Using the corrected 'prompt' keyword
                    result = client.text_generation(
                        model="tiiuae/falcon-7b-instruct",
                        prompt=full_prompt, 
                        max_new_tokens=200
                    )
                    
                    # Process the result
                    raw_reply = ""
                    if isinstance(result, str):
                        raw_reply = result
                    elif isinstance(result, list) and result and "generated_text" in result[0]:
                         raw_reply = result[0]["generated_text"]
                    else:
                        raw_reply = "Could not parse model response."
                        
                    # Clean up the reply
                    reply = raw_reply.split("assistant:")[-1].strip()
                    
                    if not reply:
                        reply = "Sorry, BudgetBuddy couldn't generate a response for that query."
                        
                except Exception as e:
                    # IMPORTANT: Print the full exception to the console for detailed debugging
                    import traceback
                    print("--- CHATBOT ERROR DETAILS ---")
                    print(traceback.format_exc())
                    print("-----------------------------")
                    
                    # Display a simplified error to the user
                    reply = "Sorry, BudgetBuddy is having trouble connecting to the model right now. Please check your **HF_TOKEN** configuration or try again later."

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
