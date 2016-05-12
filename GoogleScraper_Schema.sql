USE google_scraper;

CREATE TABLE serp (
	id INT NOT NULL AUTO_INCREMENT,
	search_engine_name varchar(20), # google, bing, yahoo, baidu, duckduckgo, ask, blekko...
	scrape_method varchar(10),#http, selenium?
	requested_at datetime,
	search_query varchar(100), #donald trump, hillary clinton

	PRIMARY KEY (id)
    );
                                    

CREATE TABLE search_engine_results (
	id INT NOT NULL AUTO_INCREMENT,
    link_type text,  # should be "results", "news_box", "image_box", "ads_main" comes from database.py as the key
    link text,
    snippet text,
	title text,
	visible_link text, # 
	rank INT, # if else statement in parser to feed into Link in database.py
    
    has_image tinyint, # 1 = has image, 0 = no image. Should populate for all "image_box" entries and first "news_box" entry
    image_height INT, # this is regex in candidate_scraper.py
    image_width INT,  # this is regex in candidate_scraperpy
    image_dims text,  # Taken from <style> in <div>, so it's text. Gets regexed 
    image_path text, # path created in candiate_scraper.py
    
    news_date text, # this is text for actual news item ... even if it was just " 4 hours ago"
    news_source text, # what was the news source
    
    PRIMARY KEY (id),
    serp_id INT,
    INDEX serp_ind (serp_id),
    FOREIGN KEY (serp_id)
		REFERENCES serp (id)
        
	);

											
SHOW tables FROM google_scraper;
SHOW columns FROM google_scraper.serp;
SHOW columns FROM google_scraper.search_engine_results;
SELECT * FROM google_scraper.search_engine_results; 
SELECT * FROM google_scraper.search_engine_results_TESTING; 
select * FROM google_scraper.serp;

# Creating new replica table for real collection
# First, rename testing table:
RENAME TABLE google_scraper.search_engine_results TO google_scraper.search_engine_results_TESTING;
# Now duplicate the TESTING table with all same cols and keys, but without the data
CREATE TABLE google_scraper.search_engine_results LIKE google_scraper.search_engine_results_TESTING;