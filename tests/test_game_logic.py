from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# check_guess
# FIX target (logic_utils.py): fixed the high/low bug — removed the
# string-comparison fallback that flipped results lexicographically, and
# aligned the hint arrows/messages with their outcomes.
# check_guess returns a tuple: (outcome, message)
# ---------------------------------------------------------------------------

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_high_message_says_go_lower():
    # Bug was a misaligned arrow/message.
    # "Too High" must tell the player to go LOWER.
    _, message = check_guess(60, 50)
    assert message == "📉 Go LOWER!"


def test_too_low_message_says_go_higher():
    _, message = check_guess(40, 50)
    assert message == "📈 Go HIGHER!"


def test_no_lexicographic_flip_single_vs_double_digit():
    # The old string-comparison fallback compared "9" > "10" as True,
    # wrongly reporting "Too High". 9 < 10 must be "Too Low".
    outcome, message = check_guess(9, 10)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_string_inputs_compared_numerically():
    # Inputs arriving as strings must still compare as numbers,
    # not lexicographically.
    assert check_guess("100", "9")[0] == "Too High"
    assert check_guess("9", "100")[0] == "Too Low"
    assert check_guess("50", "50")[0] == "Win"


# ---------------------------------------------------------------------------
# update_score
# FIX target (logic_utils.py): dropped the even/odd branch so both wrong
# outcomes are penalized consistently (-5), regardless of attempt parity.
# Signature: update_score(current_score, outcome, attempt_number)
# ---------------------------------------------------------------------------

def test_too_high_always_penalizes_regardless_of_parity():
    # Old bug: on an even attempt, "Too High" rewarded +5.
    # It must always be -5.
    assert update_score(100, "Too High", attempt_number=2) == 95   # even
    assert update_score(100, "Too High", attempt_number=3) == 95   # odd


def test_too_low_always_penalizes():
    assert update_score(100, "Too Low", attempt_number=2) == 95
    assert update_score(100, "Too Low", attempt_number=3) == 95


def test_both_wrong_outcomes_scored_the_same():
    # The two wrong outcomes must produce identical scores for the same inputs.
    for attempt in range(1, 6):
        too_high = update_score(100, "Too High", attempt)
        too_low = update_score(100, "Too Low", attempt)
        assert too_high == too_low


def test_win_awards_points():
    # Win on the first attempt should add points and increase the score.
    assert update_score(0, "Win", attempt_number=1) > 0


def test_win_points_have_floor_of_10():
    # Late wins should still award at least 10 points, never less.
    assert update_score(0, "Win", attempt_number=20) == 10


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# Newly implemented in logic_utils.py. Returns an inclusive (low, high) range.
# ---------------------------------------------------------------------------

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_range_unknown_falls_back_to_normal():
    # Any unrecognized difficulty should default to the Normal range.
    assert get_range_for_difficulty("Impossible") == (1, 100)
    assert get_range_for_difficulty("") == (1, 100)


# ---------------------------------------------------------------------------
# parse_guess
# Newly implemented in logic_utils.py. Returns (ok, guess_int, error_message).
# ---------------------------------------------------------------------------

def test_parse_valid_integer():
    assert parse_guess("42") == (True, 42, None)


def test_parse_negative_integer():
    assert parse_guess("-7") == (True, -7, None)


def test_parse_decimal_is_truncated_toward_zero():
    # Decimal strings are accepted and truncated, not rounded.
    assert parse_guess("4.9") == (True, 4, None)


def test_parse_none_is_rejected():
    ok, value, error = parse_guess(None)
    assert ok is False
    assert value is None
    assert error == "Enter a guess."


def test_parse_empty_string_is_rejected():
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None
    assert error == "Enter a guess."


def test_parse_non_numeric_is_rejected():
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error == "That is not a number."
