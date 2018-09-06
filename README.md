# ainmedl
Got sick of sending wget requests to my home server.. This is a script to download a whole graphic novel series in one go from the site http://www.kissanime.ru/

## Requirements
- pyyaml
- requests
- anime_downloader[cloudflare] <- install like this
- cfscrape
- BeautifulSoup (latest)

Just install those in order via pip and you should be good.

## Usage
`python ainmeDownloader.py <YOURLINK>` 

An example of the link could be:
`http://kissanime.ru/Anime/Violet-Evergarden`

So that would become:
`python ainmeDownloader.py http://kissanime.ru/Anime/Violet-Evergarden` 

For moving files with the auto script:

`python moveToFolder.py <CACHE YAML FILE>`

With every series download a cache file is created so the current episode that is being downloaded is saved. This allows the tool to not be dumb and re-download every episode :D

When the tool is finished it will automatically move the videos and the cache file to a folder named the title of the series. There is no need to use the move tool unless you stop downloading a series half way.

If we stopped downloading the series `http://kissanime.ru/Anime/Violet-Evergarden` at episode 5 the data in the yaml file would look like this:

`
!!python/object:animeDataStore.animeInfo {memCurrent: 5, memLength: 17, memName: Violet
    Evergarden (Sub)}
`

You are able to change the value of `memCurrent` to start downloading from another episode if need be.

In this case the cache file is called: `Violet-Evergarden-(Sub).yaml`

Thats all you have to pass in to the move tool so a final command would look like:

`python moveToFolder.py Violet-Evergarden-(Sub).yaml`

