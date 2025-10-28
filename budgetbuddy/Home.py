import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'BudgetBuddy'
)

import os
st.write("Current directory:", os.getcwd())
st.write("Files here:", os.listdir())
if os.path.exists("images/banner.png"):
    st.success("✅ Image found in this directory!")
else:
    st.error("❌ Image not found at images/banner.png")

image = Image.open('images/banner.png')
st.image(image)

st.title('Welcome to BudgetBuddy!')

st.write(
    'BudgetBuddy is your personal finance companion, designed to help you manage your expenses, track your savings, and achieve your financial goals with ease.'
)
st.write(
    'Get started by navigating through the app using the sidebar. Whether you want to track your spending, set budgets, or learn tips and tricks on saving up, BudgetBuddy has got you covered!'
)