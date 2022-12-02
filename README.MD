A Python Scrapy script to crawl the online Turkish etymological dictionary, [nisanyansozluk.com](https://www.nisanyansozluk.com/).

## How to Use

```
scrapy crawl nis -o nisanyansozluk.json --logfile log.log -s FEED_EXPORT_ENCODING=utf-8
```

### How to get wordlist:

```
Post request to: https://www.nisanyansozluk.com/api/search/advanced

Raw body:
{"word":"*"}
```
