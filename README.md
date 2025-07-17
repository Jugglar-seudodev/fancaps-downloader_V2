# Fancaps Downloader

## About <a name = "about"></a>

This project it's a simple Python script for download screencaps from https://fancaps.net.

I'm not a very experienced programmer and I only do it as a hobby

## Colab
[![Open Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1hDTnqufykos-3MNRqfZnBVisZUiCB2Io?usp=sharing)

## Getting Started <a name = "getting_started"></a>

### Prerequisites

To run this script you need to have Python 3.x installed, the Beautifulsoup4 and tqdm library:

#### python install: 
https://www.python.org/downloads/

#### Beautifulsoup4 and tqdm install: 
```
pip install beautifulsoup4 tqdm
```

## Usage <a name = "usage"></a>

### Arguments
`url`: Url of ressource to download

`--output`: Folder used for download each images

### Url support:
* `https://fancaps.net/{tv|anime}/showimages.php?...`: Url of season page
* `https://fancaps.net/{tv|anime}/episodeimages.php?...`: Url of episode page
* `https://fancaps.net/movies/MovieImages.php?...`: Url of movie page

Warning: Due to an issue with `&` caractère in args. Use double quote for the URL argument, in the case of movies, the code was updated to download page by page because if you try to download all the images, fancaps will block you for a certain time

### Example:
```
python fancaps-downloader.py --output "Download" URL
```
In this exemple we download all pics of URL into Download folder
 
