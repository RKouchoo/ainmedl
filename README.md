# ainmedl
Got sick of sending wget requests to my home server.. This is a script to download a whole graphic novel series in one go from the site http://www.kissanime.ru/

## Requirements
- pyyaml
- requests
- anime_downloader[cloudflare]
- cfscrape

Just install those in order via pip and you should be good.

## Usage
`python ainmeDownloader.py <YOUR LINK HERE>` 

An example of the link could be:
`http://kissanime.ru/Anime/Violet-Evergarden`

For moving files with the auto script:

`python moveToFolder.py <CAHCE YAML FILE>`

With every series download a cache file is created so the current episode that is being downloaded.

If we stopped downloading the series `http://kissanime.ru/Anime/Violet-Evergarden` at episode 5 the data in the yaml file would look like this:

`
!!python/object:animeDataStore.animeInfo {memCurrent: 5, memLength: 17, memName: Violet
    Evergarden (Sub)}
`

You are able to change the value of memCurrent to start downloading from another episode.

In this case the cache file is called: `Violet-Evergarden-(Sub).yaml`

Thats all you have to pass in to the move tool so a final command would look like:
`python moveToFolder.py Violet-Evergarden-(Sub).yaml`

