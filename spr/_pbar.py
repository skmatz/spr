from typing import Any, Dict, Optional


class ProgressBar:
    BAR = "■"
    EMPTY = "□"
    DELIMITER = "\t"

    def __init__(self, length: int):
        """Progress bar.

        Args:
            length (int): Progress bar length
        """
        self._length = length

        self._iter = 0
        self._num_iters: Optional[int] = None

        self._text = ""
        self._params: Dict[str, Any] = {}

    def __str__(self):
        return self._text

    def done(self):
        if self._num_iters is None:
            raise ValueError("Set `num_iters` before starting iterations.")

        self._iter += 1

        # calc bar and empty length
        rate = self._iter / self._num_iters
        bar_length = round(self._length * rate)
        empty_length = self._length - bar_length

        # format text
        self._text = (
            self.BAR * bar_length
            + self.EMPTY * empty_length
            + self.DELIMITER
            + "{:>3d}%".format(round(rate * 100))
            + self.DELIMITER
            + "[{:>3d}/{:>3d}]".format(self._iter, self._num_iters)
            + self.DELIMITER
            + self._formatter(self._params)
        )

    @property
    def num_iters(self):
        return self._num_iters

    @num_iters.setter
    def num_iters(self, num_iters: int):
        # `num_iters` can be set only once
        if self._num_iters is not None:
            raise ValueError("Value `num_iters` already set.")
        self._num_iters = num_iters

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params: Dict[str, Any]):
        self._params.update(params)

    @classmethod
    def _formatter(cls, d: Dict[str, Any]):
        string = ""
        for k, v in d.items():
            if string:
                string += cls.DELIMITER
            string += "{}: {}".format(k, v)
        return string
