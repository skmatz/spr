<p align="center">
  <a href="https://github.com/skmatz/spr">
    <img src="./assets/images/banner.png" width="1000" alt="banner" />
  </a>
</p>

<p align="center">
  <a href="./LICENSE">
    <img
      src="https://img.shields.io/github/license/skmatz/spr"
      alt="license"
    />
  </a>
  <a href="https://github.com/skmatz/spr/releases/latest">
    <img
      src="https://img.shields.io/github/v/release/skmatz/spr"
      alt="release"
    />
  </a>
</p>

<p align="center">
  <img src="./assets/images/demo.gif" width="480" alt="demo" />
</p>

## Overview

The **Slack Progress** helps you monitor your deep learning activity with Slack.

## Install

```sh
pip install git+https://github.com/skmatz/spr.git
```

## Usage

```python
from time import sleep

from spr import SlackProgress


def main():
    sp = SlackProgress()

    value = 0.0

    for _epoch in sp.progress(range(10)):
        value += 1.0
        sp.set_params({"value": value})

        sleep(1)


if __name__ == "__main__":
    main()
```

You can run [example.py](example.py) with:

```sh
TOKEN=xxx CHANNEL=yyy python example.py
```
