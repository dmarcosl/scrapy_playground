# Scrapy Playground

Example project with an implementation of the [Scrapy Framework](https://github.com/scrapy/scrapy) executed from code, handling code and request errors, and exporting the extracted data to a CSV file.

## Description

The execution is in the `app.py` file. It initializes the crawler with the options of the `spider_nest/settings.py` file, load the spiders and execute them.

The spiders extends the class `SpiderHandler` of the `spider_nest/spider_handler.py` file, which has methods to handle code and request errors, and some variables for generate statistics.

When a spider returns an object, it's catch by the `process_item()` function of the `spider_nest/pipelines.py` file, where it's written to a CSV file in the root of the project.

If an spider raises an error, it's handled by the `SpiderHandler`, and all following requests are turned down by the `DownloaderMiddleware` of the `spider_nest/middlewares.py` file, to prevent extract incomplete results (This can change according to the needs of each spider).

When the spider finish its execution, it's executed the `close_spider()` function of the `spider_nest/pipelines.py` file, where the statistics of the spider execution are printed.

## Installation

Clone the repository

```
git clone https://github.com/dmarcosl/scrapy-playground
```

Create a virtual environment and activate it

```
cd scrapy_playground
```

```
python3 -m venv venv
```

```
. venv/bin/activate
```

Install the Scrapy library

```
pip3 install -r requirements.txt
```

or

```
pip3 install scrapy==1.6.0
```

Execute it

```
python3 app.py
```
