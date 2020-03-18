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
