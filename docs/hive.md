Hive is a "pluggable software" running on top of YARN/HDFS. Its primary goal is
to facilitate reading, writing, and managing large datasets residing in distributed storage using SQL.

With Hive, it is possible to project a structure onto data already in storage and to write
__Hive Query Language (HQL)__ statements that are similar to standard SQL statements. Of course, Hive implements only a limited subset of SQL commands, but is still quite helpful.

Under the hood, HQL statement are translated into _MapReduce_ jobs and executed across a Hadoop cluster.

## Resources

This tutorial is heavily inspired from the HortonWorks tutorial and is illustrated in command-line.

* [http://hortonworks.com/hadoop-tutorial/how-to-process-data-with-apache-hive/](http://hortonworks.com/hadoop-tutorial/how-to-process-data-with-apache-hive/){: target="_blank"}

## Data Preparation

Here, we will use a CSV file with batting records, i.e. statistics about baseball players for each year.

The headers are:

playerID, yearID, stint, teamID, lgID, G ,G_batting, AB, R, H, 2B, 3B, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP, G_old

which stand for:

G=games, AB=at bats, R=runs, H=hits, 2B=doubles, 3B=triples, HR=dinger, RBI=runs batted in, SB=stolen base, CS=caught stealing, BB=base on balls, SO=strikeout, IBB=intentional walks, HBP=hit by pitch, SH=sacrifice hits, SF=sacrifice flys, GIDP=ground into double play

In this program, we will simply output the maximum number of runs made by one player for each year.

* Load the csv file [Batting.csv](resources/Batting.csv){: target="_blank"} into your home folder in HDFS:

```bash
hdfs dfs -copyFromLocal Batting.csv /user/$(whoami)
```

## Create a database in Hive

Note: In order to have this tutorial to work for everybody, let's create a database prefixed by your username (`${env:USER}` inside hive).

Type the "hive" command to start the hive shell, and continue as follows:

```bash
$ hive

create database ${env:USER}_test;
```

## Create a temp table to load the file into

```sql
$ hive

use ${env:USER}_test;
create table temp_batting (col_value STRING);
LOAD DATA INPATH '/user/${env:USER}/Batting.csv' OVERWRITE INTO TABLE temp_batting;
```

## Create the final table and insert the data into

```sql
$ hive

use ${env:USER}_test;
create table batting (player_id STRING, year INT, runs INT);
insert overwrite table batting
SELECT
regexp_extract(col_value, '^(?:([^,]*)\,?){1}', 1) player_id,
regexp_extract(col_value, '^(?:([^,]*)\,?){2}', 1) year,
regexp_extract(col_value, '^(?:([^,]*)\,?){9}', 1) run
from temp_batting;
```

## Run your first query

```sql
$ hive --database ${USER}_test

SELECT year, max(runs) FROM batting GROUP BY year;
```

## Run a more complex query

```sql
$ hive --database ${USER}_test

SELECT a.year, a.player_id, a.runs from batting a
JOIN (SELECT year, max(runs) runs FROM batting GROUP BY year ) b
ON (a.year = b.year AND a.runs = b.runs) ;
```


## Hive external table

As you might have noticed, with hive "normal" tables, you need to upload the data in HDFS,
create a temp table, load the data into this temp table, create another, final,
table and eventually copy and format the data from the temp table to the final one.

Another idea is to rely on hive external table, which will read the data directly from the CSV file.

Let's create a table mapping the CSV file and run a query on top of it.

Note: the external table location (where the data is physically stored)
**MUST** be a folder. We'll change the directory structure to accommodate this requirement.

```bash
hdfs dfs -mkdir /user/$(whoami)/Batting
hdfs dfs -copyFromLocal Batting.csv /user/$(whoami)/Batting # note here that the file needs to be re-uploaded because the LOAD DATA consumed (and removed the file)
```

And then create the external table

```sql
$ hive --database ${USER}_test

create EXTERNAL table batting_ext (player_id STRING, year INT, stint STRING, team STRING, lg STRING, G STRING, G_batting STRING, AB STRING, runs INT, H STRING, x2B STRING, x3B STRING, HR STRING, RBI STRING, SB STRING, CS STRING, BB STRING, SO STRING, IBB STRING, HBP STRING, SH STRING, SF STRING, GIDP STRING, G_Old STRING)
ROW FORMAT
DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/${env:USER}/Batting/';
```

Let's run the two queries

```sql
$ hive --database ${USER}_test

SELECT year, max(runs) FROM batting_ext GROUP BY year;

SELECT a.year, a.player_id, a.runs from batting_ext a
JOIN (SELECT year, max(runs) runs FROM batting_ext GROUP BY year ) b
ON (a.year = b.year AND a.runs = b.runs) ;
```

## Cleanup

Once you're done, you can cleanup your environment, deleting the tables and the database.

```sql
$ hive

drop table temp_batting;
drop table batting;
drop table batting_ext;
drop database ${env:USER}_test;
```


