import streamlit as st
import openai

st.title('Tips and Hacks to Save Money')
st.write(
    'Looking to save money and make the most out of your finances? This guide provides practical tips and hacks to help you cut costs and boost your savings effectively.')
tab1, tab2, tab3 = st.tabs(['Savings account', 'Good practices when shopping', 'Ask BudgetBuddy'])

with tab1:
    st.header('Fixed deposit rates')
    st.write(
        'A fixed deposit (FD) is a financial instrument provided by banks that offers a higher interest rate than a regular savings account, until the given maturity date. Here are some banks with competitive fixed deposit rates:'
    )

    st.subheader('Banks with competitive fixed deposit rates')
    st.write(
        'FD rates can vary based on the bank, the tenure of the deposit and the interest rate in the United States. Please check with the respective banks for the most up-to-date rates.'
    )
    st.write(
        'Examples include:'
    )
    st.write(
        '- United Overseas Bank (UOB)'
    )
    st.write(
        'Up to **1.20%** per annum for a **6-month** tenor, with a minimum of S$10,000.'
    )
    st.write(
        '- DBS Bank'
    )
    st.write(
        'Up to **1.60%** per annum for a **8-month** tenor, with a minimum of S$1,000.'
    )
    st.write(
        '- OCBC Bank'
    )
    st.write(
        'Up to **1.15%** per annum for a **9-month** tenor, with a minimum of S$20,000.'
    )
    
with tab2:
    st.header('Smart shopping tips')
    st.write(
        'Here are some good practices to follow when shopping to help you save money:'
    )
    st.write(
        '- Make a shopping list: Before heading out to shop, make a list of the items you need. This will help you avoid impulse purchases and stick to your budget.'
    )
    st.write(
        '- Compare prices: Take the time to compare prices across different stores or online platforms. Look for discounts, promotions, or sales that can help you get the best deal.'
    )
    st.write(
        '- Use coupons and discount codes: Look for coupons or discount codes that can be applied to your purchases. These are often found within retailer applications, such as FairPrice.'
    )
    st.write(
        '- Buy in bulk: For non-perishable items or products you use frequently, consider buying in bulk. This can often lead to cost savings in the long run.'
    )
    st.write(
        '- Avoid shopping when hungry: Shopping on an empty stomach can lead to unnecessary purchases, especially of food items. Eat before you go shopping to avoid this temptation.'
    )

    with tab3:
        st.subheader('Ask BudgetBuddy')
        st.write(
        'Ask BudgetBuddy for personalized advice and information!'
    )

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
        prompt = st.chat_input("Ask BudgetBuddy anything")
        if prompt:
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Build last 6 messages for context
            recent_msgs = st.session_state.messages[-6:]
            chat_messages = []
            for msg in recent_msgs:
                role = "user" if msg["role"] == "user" else "assistant"
                chat_messages.append({"role": role, "content": msg["content"]})

            # Generate response
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
                        st.error(f"Error from OpenAI: {e}")
                        reply = "BudgetBuddy failed to respond. Please try again."

                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

        # Reset chat button
        if st.button("Reset Chat"):
            st.session_state.messages = []
            st.experimental_rerun()

        
