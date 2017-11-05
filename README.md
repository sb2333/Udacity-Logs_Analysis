# Udacity-Logs_Analysis

## Intro To Programming Nano-Degree: Back End Development

The scope of this project was given to help develop the students SQL skills by building a reporting tool that summarizes data from a large database using **python(2.7.13) and postgresql** to answer the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Software and Files

1. Install Virtual Machine for your computer's OS (google Virtural Machines  to find links)
2. Download `newsdata` zip file [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
3. Extract file `newsdata.sql` and save it to the `vagrant` directory

## Load Data and Connect to VM
   * from vm cd to vagrant directory
   * type in cmd `vagrant up` to run vagrant on vm
   * login to vm type `vagrant ssh`
   * cd to vagrant type cmd `psql -d news -f newsdata.sql` to create and load news database

## Commands to Explore Database
   *  use `\c news` cmd to connect to news database
   *  use `\dt` cmd to display tables in database
   *  use `\dv` cmd to display views in databse
   *  use `\q` cmd to quit or logout database
   
## PSQL Views Created for Queries:
```
pop_article_Pview

CREATE view pop_article_view AS
SELECT title, count(slug) AS views
FROM articles LEFT JOIN log ON log.path LIKE concat('/article/', articles.slug) 
GROUP BY title 
ORDER BY views desc;

pop_authors_view

CREATE view pop_authors_view AS
SELECT authors.name, count(articles.author) AS views
FROM articles, log, authors
WHERE log.path LIKE concat('/article/', articles.slug) AND articles.author = authors.id
GROUP BY authors.name
ORDER BY views desc;

request_total view

CREATE view requests_total AS
SELECT date(time) as date, count(*) AS total
FROM log
GROUP BY date
ORDER BY total desc;

error_total view

CREATE view errors_total AS
SELECT date(time) AS date, count(*) AS total     
FROM log 
WHERE status != '200 OK' 
GROUP BY date 
ORDER BY total desc;

percent_error view

CREATE view percent_error AS 
SELECT to_char(r.date, 'Mon DD, YYYY'), ROUND((100.00*(e.total)/r.total),3) AS percent_error
FROM errors_total AS e, requests_total AS r 
WHERE r.date = e.date
ORDER BY r.date;
```

## Python Program
A python program `logs_anlysis.py` was created from the following psql queries:
  * SQL_query1 = select * from pop_article_view limit 3;
  * SQL_query2 = query_2 = select * from pop_authors_view;
  * SQL_query3 = query_2 = select * from pop_authors_view;

From VM, cd vagrant and run cmd `python logs_analysis.py` to get [link to output]( https://github.com/sb2333/Udacity-Logs_Analysis/blob/master/logs_output.txt)

## Acknowledgement

  * GitHub Community: Markown tutorial and code help
  * StackOverflow.com
  * W3School.com
