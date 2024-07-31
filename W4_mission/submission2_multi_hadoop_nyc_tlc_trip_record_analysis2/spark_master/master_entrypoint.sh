#!/bin/bash

# ssh service start
service ssh start

# HDFS format
export HADOOP_HOME=/opt/hadoop
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

if [ ! -d "$HADOOP_HOME/hdfs/namenode/current" ]; then
  echo "Formatting HDFS namenode..."
  $HADOOP_HOME/bin/hdfs namenode -format -force -nonInteractive
fi

echo "start namenode / resourcemanager"
$HADOOP_HOME/bin/hdfs --daemon start namenode
$HADOOP_HOME/bin/yarn --daemon start resourcemanager

$HADOOP_HOME/bin/hdfs dfs -mkdir -p /data
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /spark-logs

# spark master entrypoint
$SPARK_HOME/sbin/start-master.sh -h $SPARK_MASTER_HOST
tail -f $SPARK_HOME/logs/spark--org.apache.spark.deploy.master.Master-1-$(hostname).out