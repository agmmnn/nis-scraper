from nisanyan_crawler.crawler import main
import argparse

# parse arguments
argparser = argparse.ArgumentParser(prog="nisanyan_crawler")
argparser.add_argument(
    "words",
    type=str,
    nargs="*",
    help="[first word] [last word]",
)
argparser.add_argument("-l", "--list", action="store_true", default=True)
args = argparser.parse_args()


def cli():
    if len(args.words) == 2:
        main(args.words[0], args.words[1])
    elif len(args.words) == 1:
        main(args.words[0])
    else:
        main()


if __name__ == "__main__":
    cli()
