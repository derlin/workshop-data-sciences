TODO: redo the same kind of things in python !

Apache Zeppelin is an online notebook that let you interact with the DAPLAB cluster (or any other hadoop/spark installation) through many languages and technology backends. 

Currently, Zeppelin on the DAPLAB supports:

* Spark 1.6 and Spark 2.1.0 using python, scala or R
* Hive
* MarkDown
* Shell

# Getting Started

## Login

!!! Info
    If you are running a dockerized version of zeppelin, you can stay anonymous
    and thus skip this step.

1. Go to [Zeppelin](https://zeppelin.daplab.ch)
2. Login using your daplab credentials

## Create a new notebook

On the home page or on the notebook menu, select "_create new..._". Once the notebook is opened, give it a new name.

!!! tips "Creating folders"
    Using slashes (`/`) in the notebook name will automatically create and/or move the notebook into folders.

## Basics

A notebook is made of _cells_, also called _paragraphs_. A cell has an _interpreter_ that tells Zeppelin which langage/backend to use to run the cell.

The interpreter is configured by writing `%<interpreter name>` at the top of the cell. Without it, Zeppelin will use the default interpreter, which you can configure by clicking on <i class="fa fa-cog" aria-hidden="true"></i> _> interpreters_ at the top right of the notebook (drag-drop to re-order them, the first one being the default).

You can run cells by clicking on the <i class="fa fa-play" aria-hidden="true"></i> icon on the right or using `shift+enter`. 

Many useful shortcuts exist in edit mode. Click on <i class="fa fa-keyboard-o" aria-hidden="true"></i> the at the top right of a notebook to display them.
{: .vscc-notify-info }

## List of interpreter prefixes


| Prefix | Description |
|:-------|:------------|
| `%spark`, `%spark2` | Spark with Scala |
| `%spark.sql`, `%spark2.sql` | Spark SQL syntax |
| `%spark.dep`, `%spark2.dep` | Load dependencies for use within Spark cells | 
| `%spark.pyspark`, `%spark2.pyspark` | Spark with Python |
| `%md` | MarkDown cell |
| `%sh` | shell scripts |
| `%jdbc(hive)` | Hive |

_Note_: `spark` is Spark 1.6, `spark2` is Spark 2.1.0.

# Battling with spark

Let's use our `battling.csv` example from the [hive](https://docs.daplab.ch/tutorials/hive/){: target="_blank"} and [pig](https://docs.daplab.ch/tutorials/pig/){: target="_blank"}  tutorials. 

### Include Spark CSV

First, we need an external library to easily read the CSV. On the first cell, enter and run:

```
%dep
z.load("com.databricks:spark-csv_2.11:1.5.0")
```

`%dep` is used to manage dependencies. Have a look [here](https://zeppelin.apache.org/docs/latest/interpreter/spark.html#3-dynamic-dependency-loading-via-sparkdep-interpreter){: target="_blank" } for more information. 

If you run into the error:

```text
Must be used before SparkInterpreter (%spark) initialized
Hint: put this paragraph before any Spark code and restart Zeppelin/Interpreter
```

Open the interpretor's list (<i class="fa fa-cog" aria-hidden="true"></i> _> interpreters_ on the top right) and click on the <i class="fa fa-refresh" aria-hidden="true"></i> icon on the left of the `spark2` interpreter.

### Load Data

```
%spark2
val battingFile = "hdfs:///shared/seanlahman/2011/Batting/Batting.csv"
val batting = sqlContext.read
    .format("com.databricks.spark.csv")
    .option("header", "true") // Use first line of all files as header
    .option("inferSchema", "true") // Automatically infer data types
    .load(battingFile)
```

### Visualizing

First, have a __look at the data:__

```
%spark2
z.show(batting)
```

_NOTE_ : `z.show` is a zeppelin builtin that allows you to display values inside a variable. The interface let's you switch between views, such as table, piechart, etc.

__Compute some statistics per year__: 

```
val statsPerYear = batting
    .groupBy($"yearID")
    .agg(
        sum("R").alias("total runs"),
        sum("H").alias("total hits"), 
        sum("G").alias("total games"))

z.show(statsPerYear)
```

On the interface, select the line chart <i class="fa fa-line-chart" aria-hidden="true"></i> or area chart <i class="fa fa-area-chart" aria-hidden="true"></i> and then click on _settings_. Drag-and-drop the statistics into the _Values_ area:

![Batting with Zeppelin - statistics per year](resources/zeppelin-batting-graph.png)

__Use an input form__ to display the hit by pitch per team for a given year:

```scala
# z.input(<input name>, <default value>)
val year = z.input("year", 1894)
val hbp1894 = batting
    .filter($"yearID" === year)
    .groupBy("teamID")
    .agg(sum("HBP")
    .alias("hit by pitch"))
z.show(hbp1894)
```

`z.input` creates a simple input text. Use `z.select` for a dropdown and `z.checkbox` for multiple choices. For example, a dropdown for all teams would be:

```scala
// get all team names
val all_teams = batting.select("teamID")
    .distinct()
    .map(_.getAs[String](0))
    .collect()
// create and show a dropdown form
val team = z.select("selected team", all_teams.zip(all_teams).sorted)
```

More dynamic forms [in the documentation](https://zeppelin.apache.org/docs/latest/manual/dynamicform.html){: target="_blank" }.