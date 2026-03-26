# puwhakahua-api-client
Python client for using the Pūwhakahua API.

## Installation

The latest code straight from the repository:

```bash
pip install git+https://github.com/puwhakahua/puwhakahua-api-client.git
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
