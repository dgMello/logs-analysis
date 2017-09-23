# Logs Analysis

## Description

This python progam sends theree queires to the news database and prints out the results on a text file. The descripon of the three are queires are the following.  The queries are taken from the news database which is loaded onto the vagrant VM.
1.  The three articles with the most views.  
2.  The total views for each author.  
3.  What days had a 1% or more error rate when articles where viewed.

The program uses python code with embedded SQL code to connect to a database and get threee queries.  It then puts the results into easily readable text.  

## Installing & Running
Step 1. Use the command line to start up and and log into the Vagrant VM.

	$ cd C:/FSND-Virtual-Machine/vagrant
	$ vagrant up
	$ vagrant ssh
    
Step 3. Create the neccassry views using the views listed in the next section.

	vagrant@vagrant:~$ -psql -d news
    vagrant@vagrant:~$ create view article_views as...
    
Step 2. Navigate to the news folder.

	vagrant@vagrant:~$ cd /vagrant
	vagrant@vagrant:/vagrant$ cd news

Step 3. Enter 'python database_project.py into the command line.

	vagrant@vagrant:/vagrant/news$ python database_project.py

Step 4. Look in the news folder in your vagrant folder and open the 'News Article Queries.txt' file

## Views

There are three views that need to be created to run the querys.


1. Listing views for every article.

create view article_views as 
	select articles.author, count(*) as views 
	from articles join (select substring(path,10) as path from log) as logs
  	on articles.slug = logs.path
  	group by author;
    
2. Total aricle views.
	
  create view total_views as
  select date(time) as date, count(*) as views
  from log
  group by date;
  
3. Logs that gave a "404 NOT FOUND" error.

create view views_with_errors as select date(time) as date, count(*) as error_count
  from log where status = '404 NOT FOUND'
  group by date;


### Author

Doug Mello
