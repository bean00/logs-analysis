# Logs Analysis Project

A project for the Udacity Full Stack Web Developer Nanodegree. This project is a reporting tool that connects to a database, analyzes logs, then prints out output.

## Instructions
- Make sure the `newsdata.sql` file is in your current working directory
- Load the data and create the database & tables: <br>
```$ psql -d news -f newsdata.sql```
- Create the views, using the commands listed in the section below
- Run the python file: <br>
```$ python reporting_tool.py```

## Views to Create

Please make sure to create the necessary views using the following commands (to be entered in the PostgreSQL command-line):

```
/*
 * detailed_log: The Log table with the slug column added in
 * - Used to answer Question 1
 * - To be joined with the Articles table
 */
CREATE VIEW detailed_log AS
    SELECT *, SUBSTRING(path, 10) AS slug
      FROM log;

/*
 * author_slug: Slugs with the author's name & id
 * - Used to answer Question 2
 * - To be joined with the detailed_log table
 */
CREATE VIEW author_slug AS
    SELECT name, authors.id, slug
      FROM authors join articles
        ON authors.id = articles.author
     ORDER BY id;

/*
 * error: Days where errors were returned (# / day)
 * - Used to answer Question 3
 * - 'errors' column to be divided by 'oks' column in success view
 */
CREATE VIEW error AS
    SELECT time::date AS date, count(*) AS errors
      FROM log
     WHERE status != '200 OK'
     GROUP BY date
     ORDER BY date DESC;

/*
 * success: Days where successful responses were returned (# / day)
 * - Used to answer Question 3
 * - Divide 'errors' column from error view by 'oks' column
 */
CREATE VIEW success AS
    SELECT time::date AS date, count(*) AS oks
      FROM log
     WHERE status = '200 OK'
     GROUP BY date
     ORDER BY date DESC;
```

