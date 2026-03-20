def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIXME: Hard mode originally used a smaller range than Normal
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Updated difficulty range after reviewing bug in app behavior
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()

    if raw == "":
        return False, None, "Enter a guess."

    try:
        # FIXME: decimal inputs were silently converted instead of rejected
        if "." in raw:
            # FIX: Reject non-whole-number guesses so game input stays predictable
            return False, None, "Please enter a whole number."
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIXME: hint messages were backwards and the older version mixed ints with strings
    if guess > secret:
        # FIX: Refactored comparison logic into logic_utils.py and corrected the hint direction
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIXME: score formula depended on shifted attempt counting when attempts started at 1
        # FIX: With attempts starting at 0 in app state and incrementing on valid guesses only, this now behaves correctly
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIXME: wrong guesses previously changed score inconsistently
    if outcome == "Too High":
        # FIX: Use one consistent penalty for incorrect guesses
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score