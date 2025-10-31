import streamlit as st
from PIL import Image
import openai


with st.expander('Ask BudgetBuddy', expanded=False):
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




tab1, tab2, tab3 = st.tabs(["For the Foodie You", "For the Shopper You", "For the Adventurer You"])

with tab1: #food
    col1_first, col2_first, col3_first = st.columns(3)
    with col1_first:
        with st.expander('Use your CDC vouchers in these cafes', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7521257384853996053&index=0&sign=af0c0996d801e62ecf7d1807be933081"
            target_link = "https://www.lemon8-app.com/@ice_dwhite/7521257384853996053?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )

    with col2_first:
        with st.expander('Affordable cafe spots with good food', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7401398910469571088&index=0&sign=16c9d1eedac045424133572c79534860"
            target_link = "https://www.lemon8-app.com/@claricektx/7401398910469571088?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
    with col3_first:
        with st.expander('1-for-1 cafe mains', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7532714456204247568&index=0&sign=6a826164f3c797385cdf647c1e001faf"
            target_link = "https://www.lemon8-app.com/@puffypenguines/7532714456204247568?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )

    col1_second, col2_second, col3_second = st.columns(3)
    with col1_second:
        with st.expander('Underrated and affordable cafe perfect for locking in', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7256437281706328577&index=0&sign=170d82a856944223928ff3216c529b25"
            target_link = "https://www.lemon8-app.com/@bakeneatdiary/7522258577549967889?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
        with col2_second:
            with st.expander('Weekday lunch deals in town', expanded=True):
                image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMWD50yLDrApwitWz8o5EJGHMXW7HUqlrmXQ&s"
                target_link = "https://www.lemon8-app.com/@lilmunchyy/7546828177465950727?region=sg"  # example cafe link

                # Make image clickable
                st.markdown(
                    f"""
                    <a href="{target_link}" target="_blank">
                        <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                            onmouseover="this.style.transform='scale(1.05)'" 
                            onmouseout="this.style.transform='scale(1.0)'">
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    with col3_second:
        with st.expander('Fine dining on a budget', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7379525157645287952&index=0&sign=344a130b102e5051acd0c80ccac1dde7"
            target_link = "https://www.lemon8-app.com/@v.veliciaa2/7379525157645287952?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
    
    col1_third, col2_third, col3_third = st.columns(3)
    with col1_third:
        with st.expander('Quality Korean food for a low price', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7419249840506388993&index=0&sign=586c91466b66ee57ef5ca44560103806"
            target_link = "https://www.lemon8-app.com/@mywhole0therwrld/7419249840506388993?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
        with col2_third:
            with st.expander('Weekday lunch deals in town', expanded=True):
                image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMWD50yLDrApwitWz8o5EJGHMXW7HUqlrmXQ&s"
                target_link = "https://www.lemon8-app.com/@lilmunchyy/7546828177465950727?region=sg"  # example cafe link

                # Make image clickable
                st.markdown(
                    f"""
                    <a href="{target_link}" target="_blank">
                        <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                            onmouseover="this.style.transform='scale(1.05)'" 
                            onmouseout="this.style.transform='scale(1.0)'">
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    with col3_third:
        with st.expander('Cafes with no GST and service charge', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7519725417146909191&index=0&sign=46b6f5c127779d0a97a96ce11d803f13"
            target_link = "https://www.lemon8-app.com/@ice_dwhite/7519725417146909191?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )

with tab2: #shopping
    col1_first, col2_first, col3_first = st.columns(3)
    with col1_first:
        with st.expander('Sports shoes and branded apparel for cheap', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7352497629038641665&index=0&sign=a441dc7e9f618a6124869884c2e644d2"
            target_link = "https://www.lemon8-app.com/@myfutureisbright17/7352497629038641665?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )

    with col2_first:
        with st.expander('Cheap home accessories for interior design', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7191103364527079937&index=0&sign=63f6360b82c6a5c9186702cbefc0a1a9"
            target_link = "https://www.lemon8-app.com/@gentlebeginnings/7191103364527079937?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
    with col3_first:
        with st.expander('Cheap and good Shopee finds for the house', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7397764954943685137&index=0&sign=889b3a153347e34cd43eeac417fa7ce4"
            target_link = "https://www.lemon8-app.com/@surenlowenhouse/7397764954943685137?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )

    col1_second, col2_second, col3_second = st.columns(3)
    with col1_second:
        with st.expander('Best Taobao finds that are cheap and of quality', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7278849448380498434&index=0&sign=5e802c225153632334b0b5869c4aa2f0"
            target_link = "https://www.lemon8-app.com/@jupjiax/7278849448380498434?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
        with col2_second:
            with st.expander('Affordable Shopee accessories', expanded=True):
                image_url = "https://www.lemon8-app.com/seo/image?item_id=7258620444222177793&index=0&sign=bb00b6f5721244f86d30b9e100cd1c0b"
                target_link = "https://www.lemon8-app.com/fiona.njy/7258620444222177793?region=sg"  # example cafe link

                # Make image clickable
                st.markdown(
                    f"""
                    <a href="{target_link}" target="_blank">
                        <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                            onmouseover="this.style.transform='scale(1.05)'" 
                            onmouseout="this.style.transform='scale(1.0)'">
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    with col3_second:
        with st.expander('Clothes shopping without breaking the bank', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7305585952821363202&index=0&sign=87d3709eb0ae950a02e7e23b6c628dbb"
            target_link = "https://www.lemon8-app.com/@yuan_tiann/7305585952821363202?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
    
    col1_third, col2_third, col3_third = st.columns(3)
    with col1_third:
        with st.expander('Fashionable clothes at an affordable price', expanded=True):
            image_url = "https://p16-lemon8-sign-sg.tiktokcdn.com/tos-alisg-v-a3e477-sg/ogABB8kNALtkDzf9eCEDYEInogRQ6ANC7Mb0zA~tplv-sdweummd6v-wap-logo-v1:QGhzamJlanNqcw==:1080:0.webp?lk3s=66c60501&source=wap_large_logo_image&x-expires=1764266400&x-signature=hbzxIwJIM%2B1HKNCp9AqaeACE8UQ%3D"
            target_link = "https://www.lemon8-app.com/@hsjbejsjs/7271111928729108994?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
        with col2_third:
            with st.expander('Ungatekeeping cheap clothes that look good', expanded=True):
                image_url = "https://p16-lemon8-sign-sg.tiktokcdn.com/tos-alisg-v-a3e477-sg/oUe9gbNBNgVtnVAQALbDElCQtBIeItLLlcvgAB~tplv-sdweummd6v-wap-logo-v1:QGtlcnh1YW4=:1080:0.webp?lk3s=66c60501&source=wap_large_logo_image&x-expires=1764266400&x-signature=CUc8dsYtAe5oI7f%2FCIDmwBnr5AA%3D"
                target_link = "https://www.lemon8-app.com/kerxuan/7287064494138819074?region=sg"  # example cafe link

                # Make image clickable
                st.markdown(
                    f"""
                    <a href="{target_link}" target="_blank">
                        <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                            onmouseover="this.style.transform='scale(1.05)'" 
                            onmouseout="this.style.transform='scale(1.0)'">
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    with col3_third:
        with st.expander('Corporate fits for cheap', expanded=True):
            image_url = "https://p16-lemon8-sign-sg.tiktokcdn.com/tos-alisg-v-a3e477-sg/oUI2yQyEk61pjKq5BBEpofiD6AAChgP9iMeAxi~tplv-sdweummd6v-wap-logo-v1:QGNobG9lb2VvZW9l:1080:0.webp?lk3s=66c60501&source=wap_large_logo_image&x-expires=1764266400&x-signature=bCbs6UcVEC%2FMJYZC775NrjB1IxY%3D"
            target_link = "https://www.lemon8-app.com/@chloeoeoeoe/7347375739660009986?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )

with tab3: #adventures
    col1_first, col2_first, col3_first = st.columns(3)
    with col1_first:
        with st.expander('Sing your heart out under $10++ per pax', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7455341789097181713&index=0&sign=ef6badd25a18ae03d7b8050f892a1051"
            target_link = "https://www.lemon8-app.com/@jizztay/7455341789097181713?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )

    with col2_first:
        with st.expander('Student deals for fun activities', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7548897140337181201&index=0&sign=7f571ada165f4d62151cc439340063dc"
            target_link = "https://www.lemon8-app.com/@eaturice/7548897140337181201?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
    with col3_first:
        with st.expander('Memberships and programmes for student discounts', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7509862400401637934&index=1&sign=d1bc652c20cdd5975bd0692d0b2cb8bb"
            target_link = "https://www.lemon8-app.com/@courtneycobb5/7509862400401637934?region=us"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )

    col1_second, col2_second, col3_second = st.columns(3)
    with col1_second:
        with st.expander('Budget-friendly activities to do', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7485883636303086088&index=0&sign=41ec61137c377a2581656e6819ef8e56"
            target_link = "https://www.lemon8-app.com/@nicolepoh/7485883636303086088?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
        with col2_second:
            with st.expander('Fun activities to do for free', expanded=True):
                image_url = "https://www.lemon8-app.com/seo/image?item_id=7218517863865369090&index=0&sign=5cf923499e932911f75839620ab1e642"
                target_link = "https://www.lemon8-app.com/@yuntunmiann/7218517863865369090?region=sg"  # example cafe link

                # Make image clickable
                st.markdown(
                    f"""
                    <a href="{target_link}" target="_blank">
                        <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                            onmouseover="this.style.transform='scale(1.05)'" 
                            onmouseout="this.style.transform='scale(1.0)'">
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    with col3_second:
        with st.expander('Stamp hunting without a cost', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7514252808993374728&index=0&sign=e35ae3ffba320969bfe4e03e3dde1c81"
            target_link = "https://www.lemon8-app.com/@jergglewerggle/7514252808993374728?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
    
    col1_third, col2_third, col3_third = st.columns(3)
    with col1_third:
        with st.expander('Explore Botanic Gardens and its photo spots for free', expanded=True):
            image_url = "https://www.lemon8-app.com/seo/image?item_id=7466444039898890753&index=0&sign=2a2d7b5eaf59970cf94915fa100c7bf0"
            target_link = "https://www.lemon8-app.com/@nataniapriska/7466444039898890753?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )
        with col2_third:
            with st.expander('Free shows to watch in Gardens by the Bay', expanded=True):
                image_url = "https://www.lemon8-app.com/seo/image?item_id=7456957385463038482&index=0&sign=5c6cac091a5e1e036beec809a832f4b3"
                target_link = "https://www.lemon8-app.com/@traveldelle/7456957385463038482?region=sg"  # example cafe link

                # Make image clickable
                st.markdown(
                    f"""
                    <a href="{target_link}" target="_blank">
                        <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                            onmouseover="this.style.transform='scale(1.05)'" 
                            onmouseout="this.style.transform='scale(1.0)'">
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    with col3_third:
        with st.expander('Appreciate art at no cost', expanded=True):
            image_url = "https://p16-lemon8-sign-sg.tiktokcdn.com/tos-alisg-v-a3e477-sg/oQujIoYrxDJPeVAEAHFxDbRAH7rAOEXfQ0fL4E~tplv-sdweummd6v-wap-logo-v1:QGplbm50MDEwMQ==:1080:0.webp?lk3s=66c60501&source=wap_large_logo_image&x-expires=1764266400&x-signature=QRTPNI6rRHdO6V6%2B6OQx%2FElxYEw%3D"
            target_link = "https://www.lemon8-app.com/@jennt0101/7565052022966223381?region=sg"  # example cafe link

            # Make image clickable
            st.markdown(
                f"""
                <a href="{target_link}" target="_blank">
                    <img src="{image_url}" width="250" style="border-radius:10px; transition:transform 0.2s ease;" 
                         onmouseover="this.style.transform='scale(1.05)'" 
                         onmouseout="this.style.transform='scale(1.0)'">
                </a>
                """,
                unsafe_allow_html=True
            )