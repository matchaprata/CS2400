import streamlit as st
import openai

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

    # Initialize conversation history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Set OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # User input
    if prompt := st.chat_input("Ask BudgetBuddy anything"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Keep last 6 messages for context
        recent_msgs = st.session_state.messages[-6:]
        chat_messages = []
        for msg in recent_msgs:
            role = "user" if msg["role"] == "user" else "assistant"
            chat_messages.append({"role": role, "content": msg["content"]})

        # Generate response from OpenAI GPT-3.5
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=chat_messages,
                        temperature=0.7,
                        max_tokens=200
                    )
                    reply = response.choices[0].message.content.strip()
                except Exception as e:
                    print("ERROR:", e)
                    reply = "BudgetBuddy failed to respond. Please try again."

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

    # Optional: Reset chat button
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

    st.write("API Key loaded:", "Yes" if st.secrets["OPENAI_API_KEY"] else "No")
