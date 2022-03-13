-------

_The website has been updated and dynamic pages are not working with 'requests', for now I don't want to use 'selenium'. You can download an outdated snapshot of the site's database from here:_
https://www.kaggle.com/agmmnn/nisanyansozlukcom-database-220821 

-----------

![screenshot](https://raw.githubusercontent.com/agmmnn/nisanyan_crawler/master/ss.png)

A Python script to crawl the online Turkish etymological dictionary, [nisanyansozluk.com](https://www.nisanyansozluk.com/).

## How to Use

1. `pip install nisanyan_crawler`
2. `nisanyan_crawler [first_word] [last_word]`
    - If you want to dump whole database just use, `nisanyan_crawler`.
    - For now _first_ and _last_ words in the dictiorany are _"ab"_ <- -> _"zürriyet"_. These words are used as default in the script.

_Note: Be aware when this code was published. If the site will be updated in the future this code may not work properly._

## Structures of exported files

### output.json

```json
"word1": {
    "baslik": "",
    "tarihce": "",
    "koken": "",
    "daha_fazla": [""],
    "ek_aciklama": "",
    "benzer_sozcukler": [""],
    "maddeye_gonderenler": [""],
    "tarih": ""
},
"word2": {
...
```

### wordlist.txt

```
word1
word2
...
```

## License

CC0
