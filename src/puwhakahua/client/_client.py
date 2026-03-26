import argparse
import logging
import sys
import traceback
from io import BytesIO

from wai.logging import add_logging_level, init_logging, set_logging_level

from puwhakahua.client import ENV_PUWHAKAHUA_API_URL
from ._core import ENV_PUWHAKAHUA_LOGLEVEL, ENV_PUWHAKAHUA_API_KEY, DEFAULT_API_URL
from ._list_voices import list_voices
from ._synthesize import synthesize

CLIENT = "puwhakahua-client"

_logger = logging.getLogger(CLIENT)


def _list_voices_args(parsed: argparse.Namespace):
    """
    Lists the available voices.

    :param parsed: the parsed arguments
    :type parsed:
    :return:
    """
    set_logging_level(_logger, parsed.logging_level)
    list_voices(api_key=parsed.api_key, api_url=parsed.api_url, insecure=parsed.insecure,
                details=parsed.details,output=parsed.output, logger=_logger)


def _synthesize_args(parsed: argparse.Namespace):
    """
    Synthesizes the speech.

    :param parsed: the parsed arguments
    :type parsed:
    :return:
    """
    set_logging_level(_logger, parsed.logging_level)
    output = parsed.output
    if output is None:
        if parsed.play_audio:
            output = BytesIO()
        else:
            _logger.warning("Neither output file specified nor playing back the generated speech!")
    synthesize(parsed.voice, parsed.text, speaker=parsed.speaker, speaker_id=parsed.speaker_id,
               length_scale=parsed.length_scale, noise_scale=parsed.noise_scale, noise_w_scale=parsed.noise_w_scale,
               api_key=parsed.api_key, api_url=parsed.api_url, insecure=parsed.insecure, output=output,
               play_audio=parsed.play_audio, logger=_logger)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    init_logging(env_var=ENV_PUWHAKAHUA_LOGLEVEL)
    parser = argparse.ArgumentParser(prog=CLIENT, description="Interacts with the Pūwhakahua API for synthesizing te reo Māori speech from text.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(help='Operations help', required=True)

    subparser = subparsers.add_parser('list-voices', help='Lists the voices available for synthesis.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser.set_defaults(func=_list_voices_args)
    subparser.add_argument("-k", "--api_key", metavar="FILE", help="The text file with the API key to use, otherwise tries the " + ENV_PUWHAKAHUA_API_KEY + " environment variable.", default=None, type=str, required=False)
    subparser.add_argument("-u", "--api_url", metavar="URL", help="The custom API URL to use, otherwise checks the " + ENV_PUWHAKAHUA_API_URL + " environment variable before using the default URL (" + DEFAULT_API_URL + ").", default=None, type=str, required=False)
    subparser.add_argument("-i", "--insecure", action="store_true", help="Turns off the SSL certificate check, e.g., when using self-signed certificates.", required=False)
    subparser.add_argument("-d", "--details", action="store_true", help="Whether to output just the voices or also the configuration details of each voice.", required=False)
    subparser.add_argument("-o", "--output", metavar="FILE", help="The JSON file to store the result in instead of outputting it on stdout.", required=False, default=None)
    add_logging_level(subparser)

    subparser = subparsers.add_parser('synthesize', help='Generates speech from the supplied text.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser.set_defaults(func=_synthesize_args)
    subparser.add_argument("-k", "--api_key", metavar="FILE", help="The text file with the API key to use, otherwise tries the " + ENV_PUWHAKAHUA_API_KEY + " environment variable.", default=None, type=str, required=False)
    subparser.add_argument("-u", "--api_url", metavar="URL", help="The custom API URL to use, otherwise checks the " + ENV_PUWHAKAHUA_API_URL + " environment variable before using the default URL (" + DEFAULT_API_URL + ").", default=None, type=str, required=False)
    subparser.add_argument("-i", "--insecure", action="store_true", help="Turns off the SSL certificate check, e.g., when using self-signed certificates.", required=False)
    subparser.add_argument("-v", "--voice", metavar="ID", help="The ID of the voice model to use for synthesis.", required=True, default=None)
    subparser.add_argument("-t", "--text", metavar="TEXT", help="The text to generate audio from.", required=True, default=None)
    subparser.add_argument("-s", "--speaker", metavar="NAME", help="The name of the speaker to use (for multi-speaker models), overrides the model's default.", required=False, default=None)
    subparser.add_argument("-S", "--speaker_id", metavar="ID", help="The numeric ID of the speaker to use (for multi-speaker models), overrides the model's default.", type=int, required=False, default=None)
    subparser.add_argument("-L", "--length_scale", metavar="SCALE", help="Phoneme length scale (< 1 is faster, > 1 is slower).", type=float, required=False, default=None)
    subparser.add_argument("-n", "--noise_scale", metavar="SCALE", help="Amount of generator noise to add.", type=float, required=False, default=None)
    subparser.add_argument("-N", "--noise_w_scale", metavar="SCALE", help="Amount of phoneme width noise to add.", type=float, required=False, default=None)
    subparser.add_argument("-o", "--output", metavar="FILE", help="The WAV file to store the generated speech in. Does not need to be supplied when playing audio.", required=False, default=None)
    subparser.add_argument("-p", "--play_audio", action="store_true", help="Whether to play the generated speech as well.", required=False)
    add_logging_level(subparser)
    parsed = parser.parse_args(args=args)
    parsed.func(parsed)


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        traceback.print_exc()
        print("options: %s" % str(sys.argv[1:]), file=sys.stderr)
        return 1


if __name__ == '__main__':
    main()
