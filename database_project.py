#!/usr/bin/env python

# This python program connects to the news database
# in a the Vagrant VM gets queries for 3 differnt things.
# 1. Top three aricles views.
# 2. How many views per author.
# 3. Days that had 1% or more error percentage.

# Import the database
import psycopg2

DBNAME = 'news'


# Function to run the connect funcions and
# 3 query functions
def run_news_database_queries():
    database_connect()
    print get_top_articles()
    print get_author_views()
    print get_errors()


# Function that connects the news database.
def database_connect():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    return db, c


# Function to get top three articles and
# print the results of the query
def get_top_articles():
    db, c = database_connect()
    query1 = """select articles.title, count(*) as views
                 from articles
                 join (select substring(path,10) as path from log) as logs
                 on articles.slug = logs.path
                 group by title order by views desc limit 3;"""
    c.execute(query1)
    rows = c.fetchall()
    title1 = '        The 3 articles with the most views.'
    print title1
    for row in rows:
        print(row[0] + ' - ' + str(row[1]) + ' views')
    db.close()
    return '\n'


# Function to find the top authors and print the results of the query
def get_author_views():
    db, c = database_connect()
    query2 = """select authors.name, sum(article_views.views) as views
                from authors
                join article_views on authors.id = article_views.author
                group by authors.name
                order by views desc;"""
    c.execute(query2)
    rows = c.fetchall()
    title2 = '        Views per author.'
    print title2
    for row in rows:
        print(row[0] + ' - ' + str(row[1]) + " views")
    db.close()
    return '\n'


# Function to send a query about days with 1% or more in errors and
# print the results of the query
def get_errors():
    db, c = database_connect()
    query3 = """select total_views.date,
                (cast(views_with_errors.error_count as float) /
                cast(total_views.views as float)) * 100 as  error_percentage
                from total_views join views_with_errors
                on total_views.date = views_with_errors.date
                group by total_views.date, total_views.views,
                views_with_errors.error_count
                having (cast(views_with_errors.error_count as float) /
                cast(total_views.views as float)) * 100 >= 1
                order by error_percentage desc;"""
    c.execute(query3)
    rows = c.fetchall()
    title3 = 'Days with 1% or more errors.'
    print title3
    for row in rows:
        print(str(row[0]) + '  -  ' + "{0:.2f}".format(row[1]) + '% errors')
    db.close()
    return '\n'


run_news_database_queries()
