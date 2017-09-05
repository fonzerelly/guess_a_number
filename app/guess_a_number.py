from enum import Enum
from scratch import ScratchError
from random import randint

class GuessRatings(Enum):
    no_guess = 'no_guess'
    arctic_guess = 'arctic_guess' # difference to number larger then 20
    cold_guess = 'cold_guess' # difference to number smaler then 20
    warm_guess = 'warm_guess' # difference to number smaller then 10
    hot_guess = 'hot_guess' # difference to number smaller than 5
    winning_guess = 'winning_guess'
    error_guess = 'error_guess'

class GuessANumber:
    def __init__(self, scratch):
        self.scratch = scratch
        self.number_to_guess = 0

    def _shouldFinish(self, msg):
        return msg[0] == 'broadcast' and msg[1] == 'finish'

    def _extract_guess(self, msg):
        return msg[0] == 'sensor-update' and msg[1]['guess']

    def _rate_guess(self, guess):
        difference = abs(guess - self.number_to_guess)
        if difference > 20:
            return GuessRatings.arctic_guess
        elif difference > 10:
            return GuessRatings.cold_guess
        elif difference > 5:
            return GuessRatings.warm_guess
        elif difference != 0:
            return GuessRatings.hot_guess
        elif difference == 0:
            return GuessRatings.winning_guess

    def _handle_guess(self, msg):
        if msg[0] == 'sensor-update' and 'guess' in msg[1].keys():
            try:
                self.scratch.sensorupdate(
                    {'guess-rating': self._rate_guess(
                        self._extract_guess(msg)
                    )}
                )
            except Exception:
                self.scratch.sensorupdate(
                    {'guess-rating': GuessRatings.error_guess}
                )

    def _handle_reset(self, msg):
        if msg[0] == 'broadcast' and msg[1] == 'reset':
            self.reset()

    def random_number(self):
        self.number_to_guess = randint(1, 100)

    def hardcode_number(self, num):
        self.number_to_guess = num 

    def reset(self):
        self.random_number()
        self.scratch.sensorupdate({'guess-rating': GuessRatings.no_guess})

    def start_game(self):
        if self.number_to_guess == 0:
            self.reset()

        while True:
            msg = self.scratch.receive()
            if self._shouldFinish(msg):
                break

            self._handle_reset(msg)
            self._handle_guess(msg)
    