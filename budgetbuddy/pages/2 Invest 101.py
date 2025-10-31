import streamlit as st
import os
from huggingface_hub import InferenceClient

# Set up Hugging Face API key
# Note: In a production Streamlit Cloud environment, st.secrets["HF_TOKEN"] is the correct way
# to access the key. We ensure it's loaded here for the client initialization.
# os.environ["HF_TOKEN"] = st.secrets["HF_TOKEN"] 

# Initialize InferenceClient
# Assuming the HF_TOKEN environment variable is correctly set in the runtime environment
# For this example, we will assume st.secrets works or the token is available via the environment.
# If running locally without st.secrets, you might need to set the token directly:
# client = InferenceClient(token="YOUR_HUGGING_FACE_TOKEN_HERE")
# In the canvas environment, we rely on the environment being set up correctly.
try:
    # Use st.secrets if available (Streamlit Cloud convention)
    hf_token = st.secrets["HF_TOKEN"]
except:
    # Fallback to os.environ (standard environment variable)
    hf_token = os.environ.get("HF_TOKEN", None)

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
        # Note: This is a simple context building approach for instruction models.
        # For better performance, a dedicated chat template (e.g., in a system prompt) is recommended.
        full_prompt = '\n'.join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

        # Get AI response from Falcon 7B model
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # --- FIX APPLIED HERE ---
                    # Changed 'inputs' to the correct keyword 'prompt'
                    result = client.text_generation(
                        model="tiiuae/falcon-7b-instruct",
                        prompt=full_prompt, 
                        max_new_tokens=200
                    )
                    
                    # Hugging Face InferenceClient may return a string or a list of dicts.
                    # We adapt the parsing based on what the client returns for text generation.
                    if isinstance(result, str):
                        raw_reply = result
                    elif isinstance(result, list) and result and "generated_text" in result[0]:
                         raw_reply = result[0]["generated_text"]
                    else:
                        raw_reply = "Could not parse model response."
                        
                    # Clean up the reply, specifically removing the prompt structure the model might echo
                    reply = raw_reply.split("assistant:")[-1].strip()
                    
                    # Ensure the response is not empty
                    if not reply:
                        reply = "Sorry, BudgetBuddy couldn't generate a response for that query."
                        
                except Exception as e:
                    # Provide an informative error, but hide complex internal errors from the user
                    if "unexpected keyword argument 'inputs'" in str(e):
                        reply = "Configuration Error: The keyword for the prompt is incorrect."
                    else:
                        reply = f"Sorry, BudgetBuddy is having trouble connecting to the model right now. ({e})"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
