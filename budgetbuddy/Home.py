import streamlit as st
from PIL import Image
from pathlib import Path

st.set_page_config(page_title='BudgetBuddy')

# Always use Path to handle relative paths safely
img_path = Path(__file__).parent / "images" / "banner.png"

# Display image directly using Streamlit
st.image(str(img_path))

# If you want to open it with PIL (e.g. for resizing later)
image = Image.open(img_path)
st.image(image)

st.title('Welcome to BudgetBuddy!')

st.write(
    'BudgetBuddy is your personal finance companion, designed to help you manage your expenses, track your savings, and achieve your financial goals with ease.'
)
st.write(
    'Get started by navigating through the app using the sidebar. Whether you want to track your spending, set budgets, or learn tips and tricks on saving up, BudgetBuddy has got you covered!'
)
