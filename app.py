import streamlit as st

st.title("User profile")

st.subheader("What's your details?")

name = st.text_input("Enter your name")
email = st.text_input("Enter your email")

choice = st.selectbox("Food preference", ["Vegan", "Carnivore", "Gluten-free"])

if st.button("Submit"):
    if name and email:
        st.success("Submitted successfully!")
        st.write(name)
        st.write(email)
        st.write(choice)
    else:
        st.error("Missing details")



