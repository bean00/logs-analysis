#!/usr/bin/env python2.7

# Reporting tool
# - Answers questions about the data in the logs for a newspaper website.
#
# *Note: Must create views in order for queries to work.


import psycopg2

DB_NAME = "news"

q1_query = """
    SELECT articles.title, count(*) AS num
      FROM articles JOIN detailed_log
        ON articles.slug = detailed_log.slug
     GROUP BY articles.title
     ORDER BY num DESC
     LIMIT 3;
"""

q2_query = """
    SELECT author_slug.name, count(*) AS views
      FROM author_slug JOIN detailed_log
        ON author_slug.slug = detailed_log.slug
     GROUP BY author_slug.name
     ORDER BY views DESC;
"""

q3_query = """
    SELECT *
      FROM
           (SELECT error.date, CAST(error.errors as FLOAT) /
                   success.oks * 100 AS percent
              FROM error JOIN success
                ON error.date = success.date) AS percentages
     WHERE percentages.percent > 1;
"""


# Question 1
def answer_question_1():
    print "1. What are the most popular three articles of all time?"
    print "Running..."

    articles = execute_query(q1_query)
    print_popular_articles(articles)
    print_blank_line()


def execute_query(q1_query):
    """Execute a query"""
    db, c = connect(DB_NAME)

    c.execute(q1_query)
    results = c.fetchall()

    db.close()
    return results


def connect(database_name):
    """Connect to the database. Returns a database connection"""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)  # exit the program


def print_popular_articles(articles):
    """Print out articles and # of views in a nice format"""
    for (title, views) in articles:
        print "\"%s\" - %d views" % (title, views)


def print_blank_line():
    print ""


# Question 2
def answer_question_2():
    print "2. Who are the most popular article authors of all time?"
    print "Running..."

    authors = execute_query(q2_query)
    print_popular_authors(authors)
    print_blank_line()


def print_popular_authors(authors):
    """Print out authors and # of views in a nice format"""
    for (author, views) in authors:
        print "%s - %d views" % (author, views)


# Question 3
def answer_question_3():
    print "3. On which days did more than 1% of requests lead to errors?"
    print "Running..."

    days = execute_query(q3_query)
    print_days(days)
    print_blank_line()


def print_days(days):
    """Print out days and % of requests that were errors"""
    for (day, percent) in days:
        print "%s - %.2f%% errors" % (day, percent)


if __name__ == '__main__':
    print "This is the Logs Analysis reporting tool.\n"
    answer_question_1()
    answer_question_2()
    answer_question_3()
