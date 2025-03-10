### Description
Simple helper file to help OSUL AV lab in processing audio transcripts using whisper

### Dependencies
Python Version: 3.10-
See: https://github.com/openai/whisper
All installed dependencies are related to whisper.

At the time of this writing, Whisper doesn't appear to be fully supported in python versions beyond 3.10. \
At least, I had significant issues.  I'll revise this as I do more testing.

### Usage
$$ python whisper_helper.py -s [source directory] -d [destination directory] -m [model]

#### Options: \
Options \
-s [required]: source directory or file \
-d [required]: destination directory \
-m [optional]: model type [values: tiny, base, small,  \
                medium, large, turbo] - defaults to tiny \
-h [optional]: output usage inforamtion   
