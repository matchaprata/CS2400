import streamlit as st
from streamlit_calendar import calendar
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
import openai

st.title('Managing Expenses')

tab1, tab2, tab3 = st.tabs(['Tracker', 'Savings Goal', 'Ask BudgetBuddy'])

with tab1:
    # --- load / init ---
    if 'expenses' not in st.session_state:
        try:
            st.session_state.expenses = pd.read_csv('expenses.csv')
        except FileNotFoundError:
            st.session_state.expenses = pd.DataFrame(columns=['Date', 'Description', 'Amount', 'Note'])
    df = st.session_state.expenses

    # --- add expense ---
    with st.expander('Add New Expense'):
        with st.form('Add expense'):
            expense_date = st.date_input('Date of Expense')
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
                st.session_state.expenses.to_csv('expenses.csv', index=False)
                st.success(f'Expense added: {description} - ${amount} on {expense_date}')
                st.rerun()

    # --- build events (include 'id' = dataframe index) ---
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

    events = []
    for idx, row in st.session_state.expenses.reset_index().iterrows():
        # use the original DataFrame index as the id (so deletion maps back correctly)
        # if you reset_index above, 'index' column contains original index — use that if present
        original_index = row.get('index', idx)
        events.append({
            'id': str(original_index),
            'title': f"{row['Description']} - ${float(row['Amount']):.2f}",
            'start': str(row['Date']),
            'color': category_colours.get(str(row['Description']))
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

    # --- robust event-click handling + deletion ---
    # We try to find the clicked event info in several possible places returned by the component.
    clicked_event = None
    # Common keys that different versions might return; check them in order
    possible_paths = [
        ("eventClick", lambda s: s.get("eventClick")),
        ("event", lambda s: s.get("event")),
        ("clickedEvent", lambda s: s.get("clickedEvent")),
        ("eventClicked", lambda s: s.get("eventClicked")),
        ("events", lambda s: s.get("event") or None),
        ("eventsSet", lambda s: None),  # eventsSet used for full event list; kept for reference
    ]

    for name, fn in possible_paths:
        val = None
        try:
            val = fn(state)
        except Exception:
            val = None
        if val:
            # some shapes wrap event under 'event' or return a dict directly
            if isinstance(val, dict) and ("event" in val and isinstance(val["event"], dict)):
                clicked_event = val["event"]
            elif isinstance(val, dict) and ("id" in val or "title" in val):
                clicked_event = val
            else:
                # val could be like {"event": {...}} or other shape - try to inspect deeper
                # attempt to find first dict with 'id' in nested values
                if isinstance(val, dict):
                    for v in val.values():
                        if isinstance(v, dict) and v.get("id") is not None:
                            clicked_event = v
                            break
        if clicked_event:
            break

    # If we found a clicked_event, show confirm and delete by id
    if clicked_event:
        # defensive: id may be nested or numeric string
        event_id = clicked_event.get("id") or clicked_event.get("extendedProps", {}).get("id")
        event_title = clicked_event.get("title", "Unnamed event")
        st.warning(f"You clicked: {event_title}")
        if st.button(f"Confirm delete: {event_title}"):
            # Map id to integer index — original id saved as string of dataframe index
            try:
                idx_to_delete = int(event_id)
            except Exception:
                # sometimes id may be the position; attempt to match by title+date as fallback
                idx_to_delete = None

            if idx_to_delete is not None and (idx_to_delete in st.session_state.expenses.index):
                st.session_state.expenses = st.session_state.expenses.drop(idx_to_delete).reset_index(drop=True)
                st.session_state.expenses.to_csv('expenses.csv', index=False)
                st.success(f"Deleted: {event_title}")
                st.rerun()
            else:
                # fallback: try to find matching row by title (description + amount) and date
                # parse title into description & amount (best-effort)
                import re
                m = re.match(r"^(.*?) - \$?([\d\.,]+)", event_title)
                description_part = m.group(1).strip() if m else None
                amount_part = float(m.group(2).replace(',', '')) if (m and m.group(2)) else None

                candidate_idx = None
                for i, row in st.session_state.expenses.iterrows():
                    if description_part and description_part.lower() in str(row['Description']).lower():
                        if amount_part is None or abs(float(row['Amount']) - amount_part) < 0.01:
                            candidate_idx = i
                            break
                if candidate_idx is not None:
                    st.session_state.expenses = st.session_state.expenses.drop(candidate_idx).reset_index(drop=True)
                    st.session_state.expenses.to_csv('expenses.csv', index=False)
                    st.success(f"Deleted (fallback match): {event_title}")
                    st.rerun()
                else:
                    st.error("Could not map clicked event to an expenses row. See debug output below for the calendar state.")


    # --- pie chart (summary) ---
    if not st.session_state.expenses.empty:
        category_summary = st.session_state.expenses.groupby('Description')['Amount'].sum().to_dict()
        fig, ax = plt.subplots()
        ax.pie(list(category_summary.values()), labels=list(category_summary.keys()), autopct='%1.1f%%', startangle=90)
        st.pyplot(fig)
    else:
        st.info("No expense data to visualize yet.")


with tab2:
    with st.expander('What are you saving up for?', expanded=True):
        goal = st.radio(
            'Select a goal:',
            ['Vacation', 'Education', 'Emergency Fund', 'Others'],
            horizontal=True,
            index=None,
            key="goal_radio"  # important for session state tracking
        )

        # ✅ Reset logic: must come immediately after the radio
        if "last_goal" not in st.session_state or st.session_state.last_goal != goal:
            # Reset widget state values
            st.session_state.target_amount_vac = 0.0
            st.session_state.saved_amount_vac = 0.0
            st.session_state.target_amount_edu = 0.0
            st.session_state.saved_amount_edu = 0.0
            st.session_state.target_amount_em = 0.0
            st.session_state.saved_amount_em = 0.0
            st.session_state.target_amount_o = 0.0
            st.session_state.saved_amount_o = 0.0

            # Remember the current selection
            st.session_state.last_goal = goal
        
        if goal == 'Vacation':
            st.write(
                'How exciting! A getaway awaits you.'
            )
            target_amount_vac = st.number_input('Set your targeted amount.', min_value=0.0, format="%.2f", step=0.01, key="target_amount_vac")
            saved_amount_vac = st.number_input('How much have you saved?', min_value=0.0, format="%.2f", step=0.01, key="saved_amount_vac")
        elif goal == 'Education':
            st.write(
                'What an admirable goal! Investing in knowledge pays the best interest.'
            )
            target_amount_edu = st.number_input('Set your targeted amount.', min_value=0.0, format="%.2f", step=0.01, key="target_amount_edu")
            saved_amount_edu = st.number_input('How much have you saved?', min_value=0.0, format="%.2f", step=0.01, key="saved_amount_edu")
        elif goal == 'Emergency Fund':
            st.write(
                'Good choice! Having an emergency fund provides peace of mind during unexpected situations.'
            )
            target_amount_em = st.number_input('Set your targeted amount.', min_value=0.0, format="%.2f", step=0.01, key="target_amount_em")
            saved_amount_em = st.number_input('How much have you saved?', min_value=0.0, format="%.2f", step=0.01, key="saved_amount_em")
        elif goal == 'Others':
            st.text_area(
                'Describe your savings goal here.'
            )
            target_amount_o = st.number_input('Set your targeted amount.', min_value=0.0, format="%.2f", step=0.01, key="target_amount_o")
            saved_amount_o = st.number_input('How much have you saved?', min_value=0.0, format="%.2f", step=0.01, key="saved_amount_o")
        elif goal is None:
            st.info("Please select a savings goal to begin.")
            st.stop()

    st.subheader('Progress Tracker')
    if goal == 'Vacation':
        if target_amount_vac > 0:
            progress = min(saved_amount_vac / target_amount_vac, 1.0)  # Cap at 100%
        else:
            progress = 0.0
            
        progress_text = f"You've saved {progress*100:.2f}% of your target!"
        st.progress(progress, text=progress_text)

    elif goal == 'Education':
        if target_amount_edu > 0:
            progress = min(saved_amount_edu / target_amount_edu, 1.0)  # Cap at 100%
        else:
            progress = 0.0
            
        progress_text = f"You've saved {progress*100:.2f}% of your target!"
        st.progress(progress, text=progress_text)

    elif goal == 'Emergency Fund':
        if target_amount_em > 0:
            progress = min(saved_amount_em / target_amount_em, 1.0)  # Cap at 100%
        else:
            progress = 0.0
            
        progress_text = f"You've saved {progress*100:.2f}% of your target!"
        st.progress(progress, text=progress_text)

    else:
        if target_amount_o > 0:
            progress = min(saved_amount_o / target_amount_o, 1.0)  # Cap at 100%
        else:
            progress = 0.0
            
        progress_text = f"You've saved {progress*100:.2f}% of your target!"
        st.progress(progress, text=progress_text)

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

        
