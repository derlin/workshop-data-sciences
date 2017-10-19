
> _Déjà entendu parlé de Hadoop, Spark, Flink ou HDFS ? Curieux de savoir enfin de quoi il retourne ?_

This workshop takes place at  UNIFR / HEIA-FR the 19th and 20th of October 2017. It is organised by IT-Valley in collaboration with the DAPLAB. It is intended for any developer willing to familiarize with the Big Data and Data Sciences technologies.

Location:

- Room C00.11
- Haute école d'ingénierie et d'architecture de Fribourg
- Bd de Pérolles 80, 1705 Fribourg

It will be given in French, with support in English.


## Schedule

__Day 1__:

- Introduction: Big Data, Hadoop, HDFS, what are they ?
- HDFS: filesystem and command line usage
- MapReduce:
    * _theory_: what is MapReduce ?
    * _practice_: My first MapReduce application (java)
- Hive:
    * _theory_: what is Hive?
    * _practice_: Querying and manipulating data using Hive

__Day 2__:

- Spark and Zeppelin:
    * getting started with Zeppelin (python + pyspark)
    * Spark SQL: quick data discovery and visualisation (python + pyspark)
- LSA, _Latent Semantic Analysis_:
    * _theory_: what is it and what is it for ?
    * _practice_: implementing a document search engine using LDA, _Latent Dirichlet Allocation_ (python + pyspark)
- if there is some time left, a little tour of the DAPLAB

## Requirements

For the workshop, you will need the following:


- a laptop (Recommended: Mac or Linux)
- the Java JDK version 8 or above
- a java IDE: 
    * if you don't already have one, please install the [IntelliJ Community Edition](https://www.jetbrains.com/idea/download/)
- Maven:
    * If you have IntelliJ, you can skip this step as it already ships with an embedded Maven
    * If you want Maven available from the command line as well, follow the installation instructions on the [Maven website](https://maven.apache.org/install.html){: target="_blank"}
- Docker:
    * [Windows](https://docs.docker.com/docker-for-windows/install/){: target="_blank"} installation guide
    * [Mac](https://docs.docker.com/docker-for-mac/install/){: target="_blank"} installation guide
- Snorkel:
    - follow the instruction at [https://github.com/Sqooba/snorkel](https://github.com/Sqooba/snorkel){: target="_blank"} or have a look at the section below. 
    
        !!! warning ""
            For Windows, I added some scripts at [https://github.com/derlin/snorkel](https://github.com/derlin/snorkel){: target="_blank"}, the pull request is still in review. Use mine for now.

## Setting up Snorkel


!!! warning ""
    You need Docker running on your machine. 

Snorkel is a docker container allowing you to run Zeppelin locally.

1. Download snorkel: 

    * If you have git installed, clone the following repository: 
      ```shell
      git clone https://github.com/Sqooba/snorkel.git
      ```
    * If you don't have git installed, go to [https://github.com/Sqooba/snorkel](https://github.com/Sqooba/snorkel){: target="_blank"} 
      and select <i>Clone or download > Download ZIP</i>, then unzip.

2. open a command line and navigate inside the snorkel folder;

3. build the zeppelin image:
    * On Mac/Linux:
        ```
        ./build-images.sh
        ```
    * On Windows:
        ```
        ./build-images.cmd
        ```

4. start zeppelin:
    * On Mac/Linux:
        ```
        ./zeppelin.sh --start
        ```
    * On Windows (from the command prompt or the powershell):
        ```
        ./start-zeppelin.cmd
        ```

5. check that zeppelin is running: 
    - go to [http://localhost:8080/](http://localhost:8080/){: target="_blank"}, you should have a zeppelin welcome screen;

6. stop zeppelin:
    * On Mac/Linux:
        ```
        ./zeppelin.sh --stop
        ```
    * On Windows (from the command prompt or the powershell):
        ```
        ./stop-zeppelin.cmd
        ```
