# ytb-audio-dataset-prep
Download videos from YouTube channels, bulk-convert mp4 to wav, apply vad, and store voice only audios

*running tasks asynchronously [linux]*
```
echo 'hi' & echo 'hello' & sleep 2
```

*running tasks with gnu parallel [linux]*
**installation**
```console
sudo apt install moreutils
sudo apt install parallel
```
`tasks`
```
echo 'hi'
echo 'hello'
sleep 2
```

`parallel --jobs 6 < tasks`
