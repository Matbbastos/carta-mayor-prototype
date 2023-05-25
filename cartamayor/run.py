import json
import logging
import logging.config
from argparse import ArgumentParser
from pathlib import Path

from director import Director
from interface import welcome_users


def main(args):
    path_to_log_config = Path(
        Path(__file__).parent, "logging").with_suffix(".json").resolve()
    with open(path_to_log_config, 'r') as file_:
        config = json.load(file_)
    logging.config.dictConfig(config)
    if args.quiet == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.quiet == 2:
        logging.getLogger().setLevel(logging.WARNING)
    elif args.quiet >= 3:
        logging.getLogger().setLevel(logging.ERROR)
    logging.debug("Logger successfully started")

    welcome_users()
    director = Director()
    director.start_match()
    while director.match.ended_at is None:
        director.play_turns()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        "-q", "--quiet", action="count", default=0,
        help="quiet mode, for less outputs, stackable up to 3 times")
    try:
        main(parser.parse_args())
    except KeyboardInterrupt:
        print("\rSee ya!")
