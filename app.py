import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = difficulty

# FIXME: secret only initialized once, so changing difficulty can keep the old secret
if "secret" not in st.session_state:
    # FIX: Refactored range logic into logic_utils.py and kept secret in the correct difficulty range
    st.session_state.secret = random.randint(low, high)

# FIXME: attempts started at 1, which made attempts left incorrect before the user even guessed
if "attempts" not in st.session_state:
    # FIX: Start attempts at 0 so counting matches actual guesses made
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIXME: changing difficulty should reset the game state to match the new range
if st.session_state.current_difficulty != difficulty:
    # FIX: Reset state on difficulty change after reviewing AI suggestion and verifying in the live app
    st.session_state.current_difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

st.subheader("Make a guess")

# FIXME: UI always showed 1 to 100 instead of using the selected difficulty range
st.info(
    # FIX: Use low/high from difficulty helper so the displayed range matches the actual game
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIXME: new game only reset part of the state and always used 1 to 100
if new_game:
    # FIX: Reset secret, attempts, score, status, and history using the current difficulty range
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    # FIXME: invalid input used to consume attempts before validation happened
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    # FIXME: guesses outside the allowed range were accepted
    elif guess_int < low or guess_int > high:
        # FIX: Added explicit range validation after parsing and verified manually in Streamlit
        st.error(f"Please enter a number between {low} and {high}.")
    else:
        # FIX: Count attempts only after a valid in-range guess
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIXME: secret was previously converted to a string on some attempts, causing type bugs
        # FIX: Keep secret as an integer for all comparisons
        secret = st.session_state.secret
        outcome, message = check_guess(guess_int, secret)

        if show_hint and outcome != "Win":
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")