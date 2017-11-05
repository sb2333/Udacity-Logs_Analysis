#!/usr/bin/env python
#
#
"""Project: LOGS ANALYSIS"""


import psycopg2


def connect():

    """Try to connect to database news"""

    try:
        db = psycopg2.connect("dbname='news'")
        c = db.cursor()
        return db, c
    except psycopg2.DatabaseError:
        print "I am unable to connect to the database."

# 1. What are the most popular three articles of all time?
# Create pop_article_view

"""

create view pop_article_view as
select title, count (slug) as views
from articles left join log on log.path like concat ('%', articles.slug)
group by title
order by views desc
"""
# 2. Who are the most popular article authors of all time?
# Create pop_authors_view
"""
create view pop_authors_view as
select authors.name, count(articles.author) as views
from articles, log, authors
where log.path like concat('%', articles.slug) and articles.author = authors.id
group by authors.name
order by views desc
"""

# 3. On which days did more than 1% of requests lead to errors?
# Create 3 views to get percent_error
"""
create view requests_total as
select date(time) as date, count(*) as total
from log
group by date
order by total desc
Errors Total  view:
create view errors_total as
select date(time) as date, count(*) as total
from log
where status != '200 OK'
group by date
order by total desc
Error Percent view:
create view percent_error as
select to_char(r.date, 'Mon DD, YYYY') round((100.00*(e.total)/r.total),3)\
as percent_error
from errors_total as e, requests_total as r
where r.date = e.date
order by r.date
"""

SQL_query_1 = "select * from pop_article_view limit 3"
SQL_query_2 = "select * from pop_authors_view"
SQL_query_3 = " select * from percent_error as e where e.percent_error > 1"


def most_pop_articles(SQL_query_1):

    """Query and print results from the view created for most popular\
    articles"""

    db, c = connect()
    c.execute(SQL_query_1)
    results = c.fetchall()
    for title, views in results:
        print "\"{}\" - {} views".format(title, views)
    db.close()


def most_pop_authors(SQL_query_2):

    """Query and print the results of popular authors view created for\
    most popular authors of all time"""

    db, c = connect()
    c.execute(SQL_query_2)
    results = c.fetchall()
    for name, views in results:
        print "\"{}\" - {} views".format(name, views)
    db.close()


def percent_error(SQL_query_3):

    """Query and print results from percent errors view for days on which\
    more than 1% of requests lead to errors"""

    db, c = connect()
    c.execute(SQL_query_3)
    results = c.fetchall()
    for i in range(0, len(results), 1):
        print "\"" + str(results[i][0]) + "\" - " + str(results[i][1])\
                  + "% errors"
    db.close()


def get_query_results(query):

    """ Function will detect database error in queries"""

    try:
        db = psycopg2.connect(database="news")
        c = db.cursor()
        c.execute(query)
        result = c.fetchall()
        db.close()
        return result
    except Exception as e:
        print(e)
        exit(1)

if __name__ == '__main__':

    print "\n The results for Most Popular Articles are:\n"
    most_pop_articles(SQL_query_1)
    print("\n")
    print "\n The results for Most Popular Authors are:\n"
    most_pop_authors(SQL_query_2)
    print("\n")
    print "\n The results for days with more than 1% of errors are:\n"
    percent_error(SQL_query_3)
