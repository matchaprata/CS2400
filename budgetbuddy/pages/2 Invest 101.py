import streamlit as st
import requests

st.title('Getting started')
st.write(
    'Not sure how to begin investing? Look no further! This guide will walk you through the basics of investing, helping you make informed decisions to grow your wealth over time.'
    )
tab1, tab2 = st.tabs(['Types of Investments', 'Resources to learn more'])
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
    
        if option == 'Low':
            colour = 'green'
        elif option == 'Moderate':
            colour = 'orange'
        elif option == 'High':
            colour = 'red'
        else:
            colour = 'white'
        st.write(
            'Your risk appetite is likely:', f"<p style='color:{colour}; font-size:25px; font-weight:800;'>{option}</span></b>", unsafe_allow_html=True
        )
        
    st.subheader('Investment Options')
    if option == 'Low':
        st.write(
         'Based on your risk appetite, here are some investment options to consider:'
        )
        st.write(
            '- Bonds'
        )
        st.write(
            'A bond is a fixed-income investment product where individuals lend money to a government or company at a specified interest rate for a predetermined period.'
            'Examples include the Singapore Savings Bonds (SSB) and the United States Treasuries.'
     )
        st.write(
         '- Cash'
        )
        st.write(
         'Cash investments include savings accounts, money market accounts, and certificates of deposit (CDs). These options offer low risk and high liquidity but typically provide lower returns compared to other investment types.'
        )
    
    elif option == 'Moderate':
        st.write(
         'Based on your risk appetite, here are some investment options to consider:'
        )
        st.write(
            '- Bonds'
        )
        st.write(
            'A bond is a fixed-income investment product where individuals lend money to a government or company at a specified interest rate for a predetermined period.'
            'Examples include the Singapore Savings Bonds (SSB) and the United States Treasuries.'
     )
        st.write(
         '- Cash'
        )
        st.write(
         'Cash investments include savings accounts, money market accounts, and certificates of deposit (CDs). These options offer low risk and high liquidity but typically provide lower returns compared to other investment types.'
        )
        st.write(
            '- Mutual Funds'
        )
        st.write(
            'Mutual funds pool money from multiple investors to invest in a diversified portfolio of stocks, bonds, or other securities. They are managed by professional fund managers and offer diversification and professional management.'
            'Examples include the Vanguard 500 Index Fund and the Fidelity 500 Index Fund.'     
     )
        st.write(
         '- Exchange-Traded Funds (ETFs)'
        )
        st.write(
            'ETFs are similar to mutual funds but trade on stock exchanges like individual stocks. They offer diversification and can be bought and sold throughout the trading day.'
            'Examples include the SPDR S&P 500 ETF Trust and the Invesco QQQ ETF.'
          )
    
    elif option == 'High':
        st.write(
         'Based on your risk appetite, here are some investment options to consider:'
        )
        st.write(
            '- Bonds'
        )
        st.write(
            'A bond is a fixed-income investment product where individuals lend money to a government or company at a specified interest rate for a predetermined period.'
            'Examples include the Singapore Savings Bonds (SSB) and the United States Treasuries.'
     )
        st.write(
         '- Cash'
        )
        st.write(
         'Cash investments include savings accounts, money market accounts, and certificates of deposit (CDs). These options offer low risk and high liquidity but typically provide lower returns compared to other investment types.'
        )
        st.write(
            '- Mutual Funds'
        )
        st.write(
            'Mutual funds pool money from multiple investors to invest in a diversified portfolio of stocks, bonds, or other securities. They are managed by professional fund managers and offer diversification and professional management.'
            'Examples include the Vanguard 500 Index Fund and the Fidelity 500 Index Fund.'     
     )
        st.write(
         '- Exchange-Traded Funds (ETFs)'
        )
        st.write(
            'ETFs are similar to mutual funds but trade on stock exchanges like individual stocks. They offer diversification and can be bought and sold throughout the trading day.'
            'Examples include the SPDR S&P 500 ETF Trust and the Invesco QQQ ETF.'
          )
        st.write(
            '- Stocks'
        )
        st.write(
            'Stocks represent ownership in a company. You can profit from the increase in the share price, or earn dividends, or both. Risks vary according to the type of company you choose to buy stocks from.'     
     )
        
    else:
        st.write('Please select an option to proceed.')


with tab2:
    st.header('Want to learn more?')
    st.write(
        'Head over to these resources to deepen your understanding of investing:'
    )
    st.write(
        '- [Investopedia](https://www.investopedia.com/): A comprehensive resource for learning about various investment topics, strategies, and financial concepts.'
    )
    st.write(
        '- [SGX Academy](https://www.sgx.com/academy): Offers a range of courses and resources on investing, trading, and market analysis specifically tailored for the Singapore market.'
    )
    st.write(
        '- [MoneySense](https://www.moneysense.gov.sg/): A Singapore government initiative that provides educational resources on personal finance and investing.'
    )

    API_URL = "https://api-inference.huggingface.co/models/gpt2"
    HEADERS = {"Authorization": f"Bearer {st.secrets['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']}"}
    st.title('Ask BudgetBuddy')

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if prompt := st.chat_input("What is investing?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        full_prompt = '\n'.join([f'{m['role']}: {m['content']}' for m in st.session_state.messages])
        
    with st.chat_message('assistant'):
        with st.spinner('Thinking...'):
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={"inputs": full_prompt, 'parameters': {"max_new_tokens": 150}},
        )
            if response.status_code == 150:
                reply = response.json()[0]['generated text'].split('assistant: ')[-1].strip()
            else:
                reply = f'Error: {response.status_code} - {response.text}'
        
            st.markdown(reply)