# MinimalTemplater
Creates a minimalist blog template from a markdown files. 


## Setup
This library requires Python 3.x, plus a few other dependencies. Since it's probably better to install these 
dependencies locally for this library, setup a virtualenv and use that to install the dependency list. 

```
pip install virtualenv
virtualenv -p python3 venv
. venv/bin/activate
pip install -r conf/requirements.txt
```

## Markdown

### Markdown metadata
To facilitate some metadata, to add things like page titles, layout styles 
and all that good stuff, we'll re-use the [front-matter](https://jekyllrb.com/docs/front-matter/) style 
markdown metadata. Basically, this supports a YAML-style preamble at the 
top of each markdown page, e.g., 

```yaml
---
title: My Page Title
layout: post
tags: intro, title page, stuff
---
```


## Running HTTP Server
You can use Python 3's inbuilt http server to run the code in the html folder, once it's 
been created. To run the server, simply type, 

```
python3 -m http.server
```

### GitHub Hooks
