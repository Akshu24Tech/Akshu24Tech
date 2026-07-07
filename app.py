import streamlit as st

# Task 1: The UI Shell
st.title("Echo Chamber 9000")
st.write(
    "Welcome to the Echo Chamber. Enter your name and a message below, "
    "then press **Transmit** to send your signal into the void."
)

# Task 2: Multi-Data Collection
user_name = st.text_input("Name")
user_message = st.text_input("Message")

# Task 3: The Action Gate
if st.button("Transmit"):
    # Task 4: Conditional Routing (Edge Cases)
    if not user_name.strip():
        st.error("Please provide your name.")
    elif not user_message.strip():
        st.warning("Please type a message to transmit.")
    else:
        # Task 5: The Formatted Output
        st.success(
            f"Transmission successful! Greetings, {user_name}. "
            f"We received your message: {user_message}"
        )

        # Advanced Challenge: Token Cost Estimator
        # Heuristic from Session 1: 1 token ~ 4 characters
        char_count = len(user_message)
        token_count = char_count / 4
        st.info(
            f"System Check: Your message will consume approximately "
            f"{token_count:.1f} tokens from our context window."
        )
