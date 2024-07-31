#!/bin/bash

# ssh service start
service ssh start

# HDFS format
export HADOOP_HOME=/opt/hadoop
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

echo "start datanode / resourcemanager"
$HADOOP_HOME/bin/hdfs --daemon start datanode
$HADOOP_HOME/bin/yarn --daemon start nodemanager

$HADOOP_HOME/bin/hdfs dfs -mkdir -p /data
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /spark-logs

$SPARK_HOME/sbin/start-worker.sh spark://$SPARK_MASTER_HOST:7077
tail -f $SPARK_HOME/logs/spark--org.apache.spark.deploy.worker.Worker-1-$(hostname).out
