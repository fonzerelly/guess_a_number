import unittest
import mock

from app.guess_a_number import GuessANumber
from app.guess_a_number import GuessRatings

def scratch_message (type, content):
    return (type, content)

class MockScratchConnection:

    def __init__(self, msgs):
        self.msgs = iter(msgs)
        self.broadcast = mock.Mock(name='broadcast')
        self.sensorupdate = mock.Mock(name='sensorupdate')

    def receive(self):
        return self.msgs.next()

class TestGuessANumber(unittest.TestCase):

    def test_it_should_end_on_broadcast_finish_for_test_cases(self):
        g = GuessANumber(MockScratchConnection([
            scratch_message('broadcast', 'finish')
        ]))
        g.start_game()

    def test_it_should_init_game_by_guess_rating_no_guess(self):
        m = MockScratchConnection([
            scratch_message('broadcast', 'finish')
        ])
        g = GuessANumber(m)
        g.start_game()
        expected = [mock.call({'guess-rating': GuessRatings.no_guess})]
        self.assertEqual(m.sensorupdate.mock_calls, expected)
        

    def test_it_should_repeat_to_a_guess_with_a_guess_rating(self):
        m = MockScratchConnection([
            scratch_message('sensor-update', {'guess': 42}),
            scratch_message('broadcast', 'finish')
        ])
        g = GuessANumber(m)
        g.start_game()
        potentialRatingCalls =  map(
            lambda rating: mock.call({'guess-rating': rating}), 
            filter(
                lambda rating: rating!= GuessRatings.no_guess, 
                GuessRatings
            )
        )
        self.assertTrue(m.sensorupdate.mock_calls[1] in potentialRatingCalls)

    def _check_rating(self, randomNumber, guess, expectedRating):
        m = MockScratchConnection([
            scratch_message('sensor-update', {'guess': guess}),
            scratch_message('broadcast', 'finish')
        ])
        g = GuessANumber(m)
        g.hardcode_number(randomNumber)
        g.start_game()

        self.assertTrue(mock.call({'guess-rating': expectedRating}) in m.sensorupdate.mock_calls)

    def test_it_should_rate_a_guess_arctic_when_it_differs_further_than_20 (self):
        self._check_rating(25, 4, GuessRatings.arctic_guess)

    def test_it_should_rate_a_guess_cold_when_it_differs_less_than_20 (self):
        self._check_rating(25, 6, GuessRatings.cold_guess)

    def test_it_should_rate_a_guess_warm_when_it_differs_less_than_10 (self):
        self._check_rating(25, 16, GuessRatings.warm_guess)

    def test_it_should_rate_a_guess_hot_when_it_differs_less_than_5 (self):
        self._check_rating(25, 21, GuessRatings.hot_guess)

    def test_it_should_rate_a_guess_winning_when_it_equals_random_number (self):
        self._check_rating(25, 25, GuessRatings.winning_guess)

    def test_it_should_not_break_on_not_awaited_broadcasts(self):
        m = MockScratchConnection([
            scratch_message('broadcast', 'anything'),
            scratch_message('broadcast', 'finish')
        ])
        g = GuessANumber(m)
        g.hardcode_number(42)
        g.start_game()
        
        m.sensorupdate.assert_not_called()

    def test_it_should_not_break_on_not_awaited_sensorupdate(self):
        m = MockScratchConnection([
            scratch_message('sensor-update', {'foo': 'bar'}),
            scratch_message('broadcast', 'finish')
        ])
        g = GuessANumber(m)
        try:
            g.start_game()
        except Exception as err:
            self.fail('GuesANumber failed with error: ' + str(err))

    def test_it_should_reset_game_on_broadcast_reset(self):
        m = MockScratchConnection([
            scratch_message('broadcast', 'reset'),
            scratch_message('broadcast', 'finish')
        ])
        g = GuessANumber(m)
        g.hardcode_number(42) # ensure that reset is not called on start game
        g.start_game()

        m.sensorupdate.assert_called_with({'guess-rating': GuessRatings.no_guess})

    def test_it_should_report_on_falsy_input(self):
        m = MockScratchConnection([
            scratch_message('sensor-update', {'guess': 'meaning of life'}),
            scratch_message('broadcast', 'finish')
        ])
        g = GuessANumber(m)
        g.start_game()

        self.assertTrue(mock.call({'guess-rating': GuessRatings.error_guess}) in m.sensorupdate.mock_calls)
