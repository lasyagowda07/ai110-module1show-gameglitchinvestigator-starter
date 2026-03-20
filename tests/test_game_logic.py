from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


def test_winning_guess():
    result = check_guess(50, 50)
    assert result == ("Win", "🎉 Correct!")


def test_guess_too_high():
    result = check_guess(60, 50)
    assert result == ("Too High", "📉 Go LOWER!")


def test_guess_too_low():
    result = check_guess(40, 50)
    assert result == ("Too Low", "📈 Go HIGHER!")


def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_parse_guess_valid():
    assert parse_guess("25") == (True, 25, None)


def test_parse_guess_empty():
    assert parse_guess("") == (False, None, "Enter a guess.")


def test_parse_guess_decimal():
    assert parse_guess("5.5") == (False, None, "Please enter a whole number.")


def test_update_score_win():
    assert update_score(0, "Win", 1) == 90