# puwhakahua-python-client
Python client for using the Pūwhakahua API.

## Installation

The latest code straight from the repository:

```bash
pip install git+https://github.com/puwhakahua/puwhakahua-python-client.git
```

## Environment variables

* `PUWHAKAHUA_LOGLEVEL`: (optional) for specifying the logging level of the client
* `PUWHAKAHUA_API_KEY`: (optional) for supplying the API key 
* `PUWHAKAHUA_API_URL`: (optional) for overriding the default API URL


## Command-line

```
usage: puwhakahua-client [-h] {list-voices,synthesize} ...

Interacts with the Pūwhakahua API for synthesizing te reo Māori speech from
text.

positional arguments:
  {list-voices,synthesize}
                        Operations help
    list-voices         Lists the voices available for synthesis.
    synthesize          Generates speech from the supplied text.

options:
  -h, --help            show this help message and exit
```

### List voices

```
usage: puwhakahua-client list-voices [-h] [-k FILE] [-u URL] [-i] [-d]
                                     [-o FILE]
                                     [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

options:
  -h, --help            show this help message and exit
  -k FILE, --api_key FILE
                        The text file with the API key to use, otherwise tries
                        the PUWHAKAHUA_API_KEY environment variable. (default:
                        None)
  -u URL, --api_url URL
                        The custom API URL to use, otherwise checks the
                        PUWHAKAHUA_API_URL environment variable before using
                        the default URL (https://api.pūwhakahua.nz). (default:
                        None)
  -i, --insecure        Turns off the SSL certificate check, e.g., when using
                        self-signed certificates. (default: False)
  -d, --details         Whether to output just the voices or also the
                        configuration details of each voice. (default: False)
  -o FILE, --output FILE
                        The JSON file to store the result in instead of
                        outputting it on stdout. (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```

### Synthesize speech

```
usage: puwhakahua-client synthesize [-h] [-k FILE] [-u URL] [-i] -v ID -t TEXT
                                    [-s NAME] [-S ID] [-L SCALE] [-n SCALE]
                                    [-N SCALE] -o FILE
                                    [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

options:
  -h, --help            show this help message and exit
  -k FILE, --api_key FILE
                        The text file with the API key to use, otherwise tries
                        the PUWHAKAHUA_API_KEY environment variable. (default:
                        None)
  -u URL, --api_url URL
                        The custom API URL to use, otherwise checks the
                        PUWHAKAHUA_API_URL environment variable before using
                        the default URL (https://api.pūwhakahua.nz). (default:
                        None)
  -i, --insecure        Turns off the SSL certificate check, e.g., when using
                        self-signed certificates. (default: False)
  -v ID, --voice ID     The ID of the voice model to use for synthesis.
                        (default: None)
  -t TEXT, --text TEXT  The text to generate audio from. (default: None)
  -s NAME, --speaker NAME
                        The name of the speaker to use (for multi-speaker
                        models), overrides the model's default. (default:
                        None)
  -S ID, --speaker_id ID
                        The numeric ID of the speaker to use (for multi-
                        speaker models), overrides the model's default.
                        (default: None)
  -L SCALE, --length_scale SCALE
                        Phoneme length scale (< 1 is faster, > 1 is slower).
                        (default: None)
  -n SCALE, --noise_scale SCALE
                        Amount of generator noise to add. (default: None)
  -N SCALE, --noise_w_scale SCALE
                        Amount of phoneme width noise to add. (default: None)
  -o FILE, --output FILE
                        The WAV file to store the generated speech in.
                        (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```

## Python

The following code snippets assume the following environment variables to be set:
 
* `PUWHAKAHUA_API_KEY`
* `PUWHAKAHUA_API_URL`


### List voices

The following code queries for the available voice models and outputs the
generated list of names:

```python
import json
from io import StringIO
from puwhakahua.client import list_voices

buffer = StringIO()
if list_voices(output=buffer):
    d = json.loads(buffer.getvalue())
    print(d)
```

Full help screen for `list_voices`:

```python
list_voices(api_key: str = None, api_url: str = None, insecure: bool = False, details: bool = False, output: Union[str, _io.StringIO] = None, logger: logging.Logger = None) -> bool
    Lists the available voices.

    :param api_key: the API key to use (if necessary)
    :type api_key: str or None
    :param api_url: the API URL to use
    :type api_url: str or None
    :param insecure: whether to turn off the SSL certificate check, e.g., when using self-signed certs
    :type insecure: bool
    :param details: whether to output all the details or just the voices
    :type details: bool
    :param output: the file or StringIO to store the result in, uses stdout if None
    :type output: str or StringIO or None
    :param logger: the optional logger to use for outputting information
    :type logger: logging.Logger
    :return: True if successfully queried
    :rtype: bool
```

### Synthesize

Generate speech and play it:

```python
from puwhakahua.client import synthesize

voice = "..."
text = "..."
synthesize(voice, text, play_audio=True)
```

Generate speech and save it to a file:

```python
from puwhakahua.client import synthesize
from playsound import playsound

voice = "..."
text = "..."
if synthesize(voice, text, output="./out.wav"):
    print("Generated WAV file")
else:
    print("Something went wrong")
```

Full help screen for `synthesize`:

```python
synthesize(voice: str, text: str, speaker: str = None, speaker_id: int = None, length_scale: float = None, noise_scale: float = None, noise_w_scale: float = None, api_key: str = None, api_url: str = None, insecure: bool = False, output: Union[str, _io.BytesIO] = None, play_audio: bool = False, logger: logging.Logger = None)
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
```
