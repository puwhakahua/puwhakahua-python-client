import logging
import requests
from io import BytesIO
from typing import Union
from pydub import AudioSegment
from pydub.playback import play

from ._core import assemble_headers, get_api_url


def synthesize(voice: str, text: str, speaker: str = None, speaker_id: int = None, length_scale: float = None,
               noise_scale: float = None, noise_w_scale: float = None, api_key: str = None, api_url: str = None,
               insecure: bool = False, output: Union[str, BytesIO] = None, play_audio: bool = False,
               logger: logging.Logger = None):
    """
    Synthesizes the speech.

    :param voice: the ID of the voice model to use for synthesis
    :type voice: str
    :param text: the text to generate speech from
    :type text: str
    :param speaker: the name of the speaker to override the model's default with (when using multi-speaker models)
    :type speaker: str or None
    :param speaker_id: the ID of the speaker to override the model's default with (when using multi-speaker models)
    :type speaker_id: int or None
    :param length_scale: the phoneme length scale (< 1 is faster, > 1 is slower)
    :type length_scale: float or None
    :param noise_scale: the amount of generator noise to add
    :type noise_scale: float or None
    :param noise_w_scale: the amount of phoneme width noise to add
    :type noise_w_scale: float or None
    :param api_key: the API key to use (if necessary)
    :type api_key: str or None
    :param api_url: the API URL to use
    :type api_url: str or None
    :param insecure: whether to turn off the SSL certificate check, e.g., when using self-signed certs
    :type insecure: bool
    :param output: the file/BytesIO to write the generated WAV to
    :type output: str or BytesIO
    :param play_audio: whether to play the generated speech as well
    :type play_audio: bool
    :param logger: the optional logger to use for outputting information
    :type logger: logging.Logger
    :return: True if successfully generated
    :rtype: bool
    """
    # headers
    headers = assemble_headers(api_key=api_key, logger=logger)

    # build URL
    url = get_api_url(api_url=api_url, logger=logger)
    if url.endswith("/"):
        url = url[0:len(url)-1]
    if logger is not None:
        logger.info("Synthesizing speech using: %s" % url)

    # assemble parameters
    data = dict()
    data["voice"] = voice
    data["text"] = text
    if speaker is not None:
        data["speaker"] = speaker
    elif speaker_id is not None:
        data["speaker_id"] = speaker_id
    if length_scale is not None:
        data["length_scale"] = length_scale
    if noise_scale is not None:
        data["noise_scale"] = noise_scale
    if noise_w_scale is not None:
        data["noise_w_scale"] = noise_w_scale

    # perform request
    r = requests.post(url, headers=headers, verify=not insecure, json=data)
    if r.status_code != 200:
        if logger is not None:
            logger.error("Request failed with status code: %d" % r.status_code)
        return False

    if play_audio and (output is None):
        output = BytesIO()

    if isinstance(output, str):
        if logger is not None:
            logger.info("Writing WAV to: %s" % output)
        with open(output, "wb") as fp:
            fp.write(r.content)
        if play_audio:
            audio = AudioSegment.from_wav(output)
            play(audio)
    elif isinstance(output, BytesIO):
        output.write(r.content)
        if play_audio:
            audio = AudioSegment.from_wav(output)
            play(audio)
    elif output is None:
        if logger is not None:
            logger.warning("No output specified, cannot store generated speech!")
    else:
        raise Exception("Unsupported output type: %s" % str(type(output)))

    return True
