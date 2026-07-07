# Echo Chamber 9000 — The Identity Echo Interface

Assignment for **MirAI School of Technology — Virtual Summer Internship 2026 (AI Builder Track)**, Session 2.

An interactive Streamlit app that collects a user's name and message, validates the inputs when the **Transmit** button is clicked, and echoes back a personalized success message.

## Features (Core Requirements)

- **Task 1 — UI Shell:** Title and instructional text via `st.title()` and `st.write()`
- **Task 2 — Multi-Data Collection:** Two `st.text_input()` fields for Name and Message
- **Task 3 — Action Gate:** A single `st.button("Transmit")` gating all output logic
- **Task 4 — Conditional Routing:** `if/elif/else` handling for empty Name (`st.error`) and empty Message (`st.warning`)
- **Task 5 — Formatted Output:** f-string success message via `st.success()`

## Advanced Challenge — Token Cost Estimator

On a valid transmission, the app estimates the message's token cost using the standard heuristic (**1 token ≈ 4 characters**) and displays it with `st.info()`.

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the Local URL shown in the terminal (e.g. http://localhost:8501).

## Edge Cases Tested

- Transmit with both fields empty → error: "Please provide your name."
- Transmit with only a name, no message → warning: "Please type a message to transmit."
- Transmit with both fields filled → success message + token estimate
