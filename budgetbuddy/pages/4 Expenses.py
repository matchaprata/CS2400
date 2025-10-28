import streamlit as st
from streamlit_calendar import calendar
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date

st.title('Managing Expenses')

tab1, tab2 = st.tabs(['Tracker', 'Savings Goal'])

# --- Session State Setup ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Description', 'Amount', 'Note'])

df = st.session_state.expenses

with tab1:
    # --- Add Expense ---
    with st.expander('Add New Expense'):
        with st.form('Add expense'):
            expense_date = st.date_input('Date of Expense', value=date.today())
            description = st.radio(
                'Description',
                ['Groceries', 'Utilities', 'Food', 'Transport', 'Entertainment', 'Others'],
                horizontal=True
            )
            amount = st.number_input('Amount', min_value=0.0, format="%.2f", step=0.01)
            note = st.text_area('Note (optional)')
            submitted = st.form_submit_button('Add Expense')
            if submitted:
                new_entry = pd.DataFrame([{
                    'Date': expense_date,
                    'Description': description,
                    'Amount': amount,
                    'Note': note
                }])
                st.session_state.expenses = pd.concat([st.session_state.expenses, new_entry], ignore_index=True)
                st.success(f'Expense added: {description} - ${amount:.2f} on {expense_date}')
                st.rerun()

    # --- Calendar Mode Selection ---
    mode = st.selectbox(
        "📆 Calendar Mode",
        ["Month", "Week", "Schedule", "Year"],
        index=0
    )

    # --- Calendar Config ---
    calendar_view_map = {
        "Month": "dayGridMonth",
        "Week": "timeGridWeek",
        "Schedule": "listMonth",
        "Year": "multiMonthYear"
    }

    calendar_options = {
        "initialView": calendar_view_map[mode],
        "editable": True,
        "navLinks": True,
        "selectable": True,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,listMonth,multiMonthYear"
        },
    }

    category_colours = {
        'Groceries': 'green',
        'Utilities': 'orange',
        'Food': 'blue',
        'Transport': 'black',
        'Entertainment': 'purple',
        'Others': 'brown'
    }

    # --- Build Events ---
    events = []
    for idx, row in st.session_state.expenses.reset_index().iterrows():
        original_index = row.get('index', idx)
        events.append({
            'id': str(original_index),
            'title': f"{row['Description']} - ${float(row['Amount']):.2f}",
            'start': str(row['Date']),
            'color': category_colours.get(str(row['Description']), 'gray')
        })

    st.subheader("Expense Calendar")
    state = calendar(
        events=events,
        options=calendar_options,
        custom_css="""
            .fc-event-title { font-weight: 700; }
            .fc-toolbar-title { font-size: 1.4rem; }
        """,
        key="expense_calendar",
    )

    # --- Event Click/Delete Handling ---
    clicked_event = None
    if isinstance(state, dict):
        for key in ["eventClick", "event", "clickedEvent", "eventClicked"]:
            if key in state and state[key]:
                val = state[key]
                if isinstance(val, dict) and 'id' in val:
                    clicked_event = val
                    break

    if clicked_event:
        event_id = clicked_event.get("id")
        event_title = clicked_event.get("title", "Unnamed event")
        st.warning(f"You clicked: {event_title}")
        if st.button(f"Confirm delete: {event_title}"):
            try:
                idx_to_delete = int(event_id)
                if idx_to_delete in st.session_state.expenses.index:
                    st.session_state.expenses = st.session_state.expenses.drop(idx_to_delete).reset_index(drop=True)
                    st.success(f"Deleted: {event_title}")
                    st.rerun()
            except Exception:
                st.error("Could not delete event.")

    # --- Pie Chart ---
    if not st.session_state.expenses.empty:
        category_summary = st.session_state.expenses.groupby('Description')['Amount'].sum().to_dict()
        fig, ax = plt.subplots()
        ax.pie(list(category_summary.values()), labels=list(category_summary.keys()), autopct='%1.1f%%', startangle=90)
        st.pyplot(fig)
    else:
        st.info("No expense data to visualize yet.")


# ---------------- TAB 2: Savings Goal ----------------
with tab2:
    with st.expander('What are you saving up for?', expanded=True):
        goal = st.radio(
            'Select a goal:',
            ['Vacation', 'Education', 'Emergency Fund', 'Others'],
            horizontal=True,
            index=None,
            key="goal_radio"
        )

        if "last_goal" not in st.session_state or st.session_state.last_goal != goal:
            # reset values when switching goals
            for key in [
                "target_amount_vac", "saved_amount_vac",
                "target_amount_edu", "saved_amount_edu",
                "target_amount_em", "saved_amount_em",
                "target_amount_o", "saved_amount_o"
            ]:
                st.session_state[key] = 0.0
            st.session_state.last_goal = goal

        if goal == 'Vacation':
            st.write('How exciting! A getaway awaits you.')
            target = st.number_input('Target Amount', 0.0, format="%.2f", key="target_amount_vac")
            saved = st.number_input('Saved Amount', 0.0, format="%.2f", key="saved_amount_vac")

        elif goal == 'Education':
            st.write('What an admirable goal! Investing in knowledge pays the best interest.')
            target = st.number_input('Target Amount', 0.0, format="%.2f", key="target_amount_edu")
            saved = st.number_input('Saved Amount', 0.0, format="%.2f", key="saved_amount_edu")

        elif goal == 'Emergency Fund':
            st.write('Good choice! Having an emergency fund provides peace of mind.')
            target = st.number_input('Target Amount', 0.0, format="%.2f", key="target_amount_em")
            saved = st.number_input('Saved Amount', 0.0, format="%.2f", key="saved_amount_em")

        elif goal == 'Others':
            st.text_area('Describe your savings goal here.')
            target = st.number_input('Target Amount', 0.0, format="%.2f", key="target_amount_o")
            saved = st.number_input('Saved Amount', 0.0, format="%.2f", key="saved_amount_o")

        else:
            target = 0.0
            saved = 0.0
            st.info('Please select an option to proceed.')

    st.subheader('Progress Tracker')
    if target > 0:
        progress = min(saved / target, 1.0)
        progress_text = f"You've saved {progress*100:.2f}% of your target!"
        st.progress(progress, text=progress_text)
    else:
        st.info("Set a target amount to start tracking your savings progress.")
