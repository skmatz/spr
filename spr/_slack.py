import os
from typing import Optional

import requests


class _SlackAPIError(Exception):
    pass


class Slack:
    def __init__(self, token: Optional[str] = None, channel: Optional[str] = None):
        """Slack client.

        Args:
            token (Optional[str], optional): Slack Bot User OAuth Access Token. This token must have permission:
                `chat:write`. If this argument is `None`, get the 'TOKEN' value from the environment variable
                automatically. Defaults to None.
            channel (Optional[str], optional): Slack channel ID to post. If this argument is `None`, get the 'CHANNEL'
                value from the environment variable automatically. Defaults to None.

        Raises:
            ValueError: If `token` and `channel` could not be obtained from arguments or environment variables, raise
                `ValueError`.
        """
        if token is None:
            token = os.getenv("TOKEN")

        if channel is None:
            channel = os.getenv("CHANNEL")

        if token is None or channel is None:
            raise ValueError("Enter token and channel as environment variables or arguments.")

        self._token = token
        self._channel = channel

        self._timestamp: Optional[int] = None

    def post(self, text: str):
        """Post to Slack.

        After posting, timestamp is stored.

        Args:
            text (str): Message content

        Raises:
            _SlackAPIError: If the Slack API returns an error, raise `_SlackAPIError`.
        """
        payload = {
            "token": self._token,
            "channel": self._channel,
            "text": text,
        }
        r = requests.post(url="https://slack.com/api/chat.postMessage", data=payload).json()

        if not r["ok"]:
            raise _SlackAPIError(f"Slack API error: `{r['error']}` occurred.")

        # store timestamp for editting
        self._timestamp = r["message"]["ts"]

    def update(self, text: str):
        """Edit latest post.

        Args:
            text (str): Message content.

        Raises:
            ValueError: If the `post` method has not been called and the `timestamp` has not been stored, raise
                `ValueError`.
            _SlackAPIError: If the Slack API returns an error, raise `_SlackAPIError`.
        """
        if self._timestamp is None:
            raise ValueError("Execute `post` method at least once, and then execute this `update` method.")

        payload = {
            "token": self._token,
            "channel": self._channel,
            "text": text,
            "ts": self._timestamp,
        }
        r = requests.post(url="https://slack.com/api/chat.update", data=payload).json()

        if not r["ok"]:
            raise _SlackAPIError(f"Slack API error: `{r['error']}` occurred.")
