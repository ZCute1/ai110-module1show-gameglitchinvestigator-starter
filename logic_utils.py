"""Pure game-logic helpers for the Game Glitch Investigator guessing game.

These functions hold no UI or session state so they can be unit-tested in
isolation from the Streamlit app in ``app.py``.
"""


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"``.

    Returns:
        A ``(low, high)`` tuple of ints giving the inclusive bounds the
        secret number may fall within. Unrecognized values fall back to the
        ``"Normal"`` range of ``(1, 100)``.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """Parse raw user input into an integer guess.

    Accepts plain integers as well as decimal strings, which are truncated
    toward zero (e.g. ``"4.9"`` becomes ``4``).

    Args:
        raw: The raw text entered by the player. May be ``None`` or empty.

    Returns:
        A ``(ok, guess_int, error_message)`` tuple:

        * ``ok`` (bool): ``True`` if parsing succeeded, ``False`` otherwise.
        * ``guess_int`` (int | None): The parsed value, or ``None`` on failure.
        * ``error_message`` (str | None): A human-readable reason on failure,
          or ``None`` on success.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess to the secret and report the result.

    Both arguments are coerced to ``int`` before comparison so that
    string-typed inputs (e.g. ``"9"``) are compared numerically rather than
    lexicographically.

    Args:
        guess: The player's guess (int or numeric string).
        secret: The secret number (int or numeric string).

    Returns:
        An ``(outcome, message)`` tuple where ``outcome`` is one of
        ``"Win"``, ``"Too High"``, or ``"Too Low"`` and ``message`` is the
        matching player-facing hint. The hint's direction always agrees with
        the outcome (too high -> go lower, too low -> go higher).
    """
    # FIX: Moved check_guess from app.py into logic_utils.py and fixed the
    # high/low bug — removed the string-comparison fallback (which flipped
    # results lexicographically) and aligned arrows with outcomes
    # (using agent mode)
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Compute the new score after a guess.

    A win awards ``100 - 10 * (attempt_number + 1)`` points, floored at 10, so
    quicker wins score higher while every win earns at least 10. Any wrong
    guess (too high or too low) deducts 5 points. Unrecognized outcomes leave
    the score unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: The outcome from :func:`check_guess`.
        attempt_number: The 1-based attempt count, used to scale the win bonus.

    Returns:
        The updated score as an int.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Moved update_score from app.py and dropped the even/odd branch so
    # both wrong outcomes are penalized consistently (-5) (using agent mode)
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
