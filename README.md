# Flat Rent Information Scraper

This project uses Scrapy to scrape data related to flat rentals from rieltor.ua website. The gathered data is then processed using pandas for data cleaning and transformation, followed by visualization with seaborn to provide insights into the rental market.

## Overview

The goal of this project is to collect detailed information on flat rentals including but not limited to price, location, size, and amenities. Once collected, the data undergoes preprocessing steps where missing values are handled, and relevant features are extracted or engineered. Finally, we employ seaborn, a powerful Python visualization library based on matplotlib, to create meaningful visualizations that help understand trends within the rental market better <button class="citation-flag" data-index="2">.

## Technologies Used

- **Scrapy**: For web scraping purposes, extracting structured data from websites.
- **PostgreSQL** : A robust relational database used for storing the scraped data securely and efficiently.
- **Pandas**: Utilized for data manipulation and analysis after the data has been scraped .
- **Seaborn**: Employed for creating informative and attractive statistical graphics .

## Features

- Automated data collection via Scrapy spiders targeting real estate platform.
- Comprehensive data processing pipeline implemented through Scrapy’s Item Pipelines which leverages pandas for efficient data handling.
- Persistent Data Storage : PostgreSQL ensures reliable and scalable storage of the scraped data.
- Advanced data visualization capabilities provided by seaborn, enabling deeper insights into the rental data patterns .

## How It Works

1. **Data Collection**: Scrapy spiders crawl designated website collecting pertinent details about available flats for rent.
2. **Data Processing**: Raw data obtained from crawling is cleaned and transformed using pandas; operations include removing duplicates, filling missing values, etc.
3. **Visualization**: Processed datasets are visualized using seaborn to highlight important aspects such as average prices per area, distribution of property sizes, and more.

