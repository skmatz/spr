from typing import Any, Dict, Optional

from typing_extensions import Protocol

from ._pbar import ProgressBar
from ._slack import Slack


class _SizedIterable(Protocol):
    def __len__(self):
        pass

    def __iter__(self):
        pass


class SlackProgress:
    def __init__(
        self, length=20, token: Optional[str] = None, channel: Optional[str] = None,
    ):
        """Client.

        Args:
            length (int, optional): Progress bar length. Defaults to 20.
            token (Optional[str], optional): Slack Bot User OAuth Access Token. This token must have permission:
                `chat:write`. If this argument is `None`, get the 'TOKEN' value from the environment variable
                automatically. Defaults to None.
            channel (Optional[str], optional): Slack channel ID to post. If this argument is `None`, get the 'CHANNEL'
                value from the environment variable automatically. Defaults to None.
        """
        self._pbar = ProgressBar(length=length)
        self._slack = Slack()

    def progress(self, iterable: _SizedIterable):
        """Iterate Slack Progress.

        Args:
            iterable (_SizedIterable): Iterable objects
        """
        if self._pbar.num_iters is None:
            self._pbar.num_iters = len(iterable)

        for idx, obj in enumerate(iterable):
            yield obj
            self._pbar.done()

            if idx == 0:
                self._slack.post(str(self._pbar))
            else:
                self._slack.update(str(self._pbar))

    def set_params(self, params: Dict[str, Any]):
        """Set additional parameters to progress bar.

        Args:
            params (Dict[str, Any]): Additional parameters. Internally, dictionally is updated.
        """
        self._pbar.params = params
