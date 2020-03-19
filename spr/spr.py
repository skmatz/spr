import datetime as dt
import os
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
        self,
        length=20,
        token: Optional[str] = None,
        channel: Optional[str] = None,
        summary: Optional[str] = "{time} {params}",
    ):
        """Client.

        Args:
            length (int, optional): Progress bar length. Defaults to 20.
            token (Optional[str], optional): Slack Bot User OAuth Access Token. This token must have permission:
                `chat:write`. If this argument is `None`, get the 'TOKEN' value from the environment variable
                automatically. Defaults to None.
            channel (Optional[str], optional): Slack channel ID to post. If this argument is `None`, get the 'CHANNEL'
                value from the environment variable automatically. Defaults to None.
            summary (Optional[str], optional): Iterate summary format.
                Available parameters:
                    {time}: Execution time
                    {params}: Last params of iterate
                Defaults to "{time} {params}".
        """
        self._token = os.getenv("TOKEN") if token is None else token
        self._channel = os.getenv("CHANNEL") if channel is None else channel

        self._pbar = ProgressBar(length=length)
        self._slack = Slack(token=self._token, channel=self._channel)
        self._summary = summary

        self._t1: Optional[dt.datetime] = None
        self._t2: Optional[dt.datetime] = None

    def progress(self, iterable: _SizedIterable):
        """Iterate Slack Progress.

        Args:
            iterable (_SizedIterable): Iterable objects
        """
        if self._pbar.num_iters is None:
            self._pbar.num_iters = len(iterable)

        self._t1 = dt.datetime.now()

        for idx, obj in enumerate(iterable):
            yield obj
            self._pbar.done()

            if idx == 0:
                self._slack.post(str(self._pbar))
            else:
                self._slack.update(str(self._pbar))

        self._t2 = dt.datetime.now()
        self._post_summary()

    def set_params(self, params: Dict[str, Any]):
        """Set additional parameters to progress bar.

        Args:
            params (Dict[str, Any]): Additional parameters. Internally, dictionally is updated.
        """
        self._pbar.params = params

    def _post_summary(self):
        slack = Slack(token=self._token, channel=self._channel)

        def fmt(td: dt.timedelta) -> str:
            return "".join(str(td).split(".")[:-1])

        td = self._t2 - self._t1
        params = self._pbar.params
        summary = self._summary.format(time=fmt(td), params=params)

        slack.post(summary)
