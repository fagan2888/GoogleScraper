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
SELECT * FROM google_scraper.serp_TESTING;
SELECT * from google_scraper.search_engine_results_TESTING WHERE link_type = 'results' AND content_HTML is NULL LIMIT 125;
SELECT count * search_results_dec15;
SELECT * FROM google_scraper.search_engine_results WHERE link_type = 'image_box' AND serp_id > 3093 AND serp_id <3400;# INTO OUTFILE './image_box.csv';

SELECT * FROM google_scraper.search_engine_results WHERE serp_id > 10000;# INTO OUTFILE './image_box.csv';
SELECT * FROM google_scraper.serp WHERE serp.requested_at = 2016-12-01;


# Creating new replica table for real collection
# First, rename testing table:
RENAME TABLE google_scraper.search_engine_results TO google_scraper.search_engine_results_TESTING;
RENAME TABLE google_scraper.serp TO google_scraper.serp_TESTING;

# Now duplicate the TESTING table with all same cols and keys, but without the data
CREATE TABLE google_scraper.search_engine_results LIKE google_scraper.search_engine_results_TESTING;
CREATE TABLE google_scraper.serp LIKE google_scraper.serp_TESTING;
#DROP TABLE google_scraper.search_engine_results;

ALTER TABLE google_scraper.search_engine_results_TESTING ADD COLUMN content_HTML longtext;
ALTER TABLE google_scraper.search_engine_results_TESTING ADD COLUMN content_text longtext;
ALTER TABLE google_scraper.search_engine_results_TESTING ADD COLUMN doc_sentiment varchar(100);
ALTER TABLE google_scraper.search_engine_results_TESTING ADD COLUMN doc_score decimal(10,9);
ALTER TABLE google_scraper.search_engine_results_TESTING ADD COLUMN doc_mixed int(11);
ALTER TABLE google_scraper.search_engine_results_TESTING ADD COLUMN grab_datetime datetime;
ALTER TABLE google_scraper.search_engine_results_TESTING ADD COLUMN top_stories text;

INSERT INTO  search_engine_results_TESTING (content_HTML, content_text, doc_sentiment, doc_score, doc_mixed, grab_datetime) VALUES (content_HTML, content_text, doc_sentiment, doc_score, doc_mixed, grab_datetime);
UPDATE search_engine_results_TESTING SET content_HTML = content_HTML;
UPDATE search_engine_results_TESTING SET content_HTML = content_HTML,content_text = content_text,doc_sentiment = doc_sentiment,doc_score = doc_score,doc_mixed = doc_mixed, grab_datetime = grab_datetime;

ALTER TABLE google_scraper.search_engine_results ADD COLUMN content_HTML longtext;
ALTER TABLE google_scraper.search_engine_results ADD COLUMN content_text longtext;
ALTER TABLE google_scraper.search_engine_results ADD COLUMN doc_sentiment varchar(100);
ALTER TABLE google_scraper.search_engine_results ADD COLUMN doc_score decimal(10,9);
ALTER TABLE google_scraper.search_engine_results ADD COLUMN doc_mixed int(11);
ALTER TABLE google_scraper.search_engine_results ADD COLUMN grab_datetime datetime;