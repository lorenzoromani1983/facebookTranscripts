# facebookTranscripts
A simple (work in progress) script to extract transcripts from Google-indexed Facebook videos containing high quality transcripts

Most Facebook videos, live videos, etc that are indexed by Google contain a metadata json embedded into the html. This json has a lot of information about the video, including
a full transcript.

I've found Facebook's transcripts to be really accurate, perhaps much more accurate than what can be achieved by passing the audio through Google's speech to text free API.
In order to run the script, just pass it through your Python3 coommand line:

>>> python3 facebookTranscripts.py

then you'll need to specify the query you're looking for. You can also use search operators to refine it:

intitle: "human trafficking" -police
inurl: "human-trafficking-investigation"
...


The file outputs a csv containing, besides the transcript, other informations about the video (published date; comments count; raw video url, etc)
Some videos will not contain any transcript; some will be longer than 32700 characters, the maximum lenght that Excel allows to visualize in a single cell. In this case, the ouptut csv
will likely break if opened into Excel.

So I recommend using a Pandas dataframe to parse, read and search through the file:

>>> import pandas as pd

>>> df = pd.read_csv("path-to-facebookTranscripts.csv", delimiter = "|", encoding = "Latin1")

>>> "slavery" in df['Transcript']

>>> True

leave a comment for any question/suggestion!

