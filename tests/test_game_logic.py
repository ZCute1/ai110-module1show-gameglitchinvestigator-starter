from logic_utils import check_guess, update_score


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
    # Bug was a misaligned arrow/message. "Too High" must tell the player to go LOWER.
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
    # Inputs arriving as strings must still compare as numbers, not lexicographically.
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
    # Old bug: on an even attempt, "Too High" rewarded +5. It must always be -5.
    assert update_score(100, "Too High", attempt_number=2) == 95   # even
    assert update_score(100, "Too High", attempt_number=3) == 95   # odd


def test_too_low_always_penalizes():
    assert update_score(100, "Too Low", attempt_number=2) == 95
    assert update_score(100, "Too Low", attempt_number=3) == 95


def test_both_wrong_outcomes_scored_the_same():
    # The two wrong outcomes must produce identical scores for the same inputs.
    for attempt in range(1, 6):
        assert update_score(100, "Too High", attempt) == update_score(100, "Too Low", attempt)


def test_win_awards_points():
    # Win on the first attempt should add points and increase the score.
    assert update_score(0, "Win", attempt_number=1) > 0


def test_win_points_have_floor_of_10():
    # Late wins should still award at least 10 points, never less.
    assert update_score(0, "Win", attempt_number=20) == 10
