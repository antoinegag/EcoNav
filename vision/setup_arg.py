import argparse


def setup():
    ap = argparse.ArgumentParser()

    # Logging
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("-d", "--debug", action="store_true")

    # Saving
    ap.add_argument(
        "-s", "--save", help="Save processed video", action="store_true")

    ap.add_argument("-r", "--record",
                    help="Save raw video", action="store_true")

    ap.add_argument(
        "--outdir", help="Directory to save the processed video", default="./out/")

    ap.add_argument("--src", help="Source for the video feed, url or filename",
                    default="http://econav.local:8000/stream.mjpg")

    # Display
    ap.add_argument(
        "--displayraw", help="Display raw footage", action="store_true")

    ap.add_argument("--headless", help="Do not display anything",
                    action="store_true")

    # Cascade settings
    ap.add_argument("--scalefactor", default=1.15)
    ap.add_argument("--minneighbors", default=6)

    # Misc
    ap.add_argument("--brand", action="store_true")

    return vars(ap.parse_args())
