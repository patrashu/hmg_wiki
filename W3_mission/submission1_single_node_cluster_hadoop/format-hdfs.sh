
su - hdfs -c '
  export HADOOP_COMMON_LIB_NATIVE_DIR=$/opt/hadoop/lib/native$
  if [ ! -d "/opt/hadoop/hdfs/namenode/current" ]; then
    echo "Formatting HDFS namenode..."
    /opt/hadoop/bin/hdfs namenode -format -force -nonInteractive
  fi
  
  echo "Starting HDFS namenode..."
  /opt/hadoop/sbin/hadoop-daemon.sh start namenode

  echo "Starting HDFS datanode..."
  /opt/hadoop/sbin/hadoop-daemon.sh start datanode

  echo "Starting HDFS secondary namenode..."
  /opt/hadoop/sbin/hadoop-daemon.sh start secondarynamenode
'

su - yarn -c '
  echo "Starting YARN ResourceManager..."
  /opt/hadoop/sbin/yarn-daemon.sh start resourcemanager

  echo "Starting YARN NodeManager..."
  /opt/hadoop/sbin/yarn-daemon.sh start nodemanager
'

tail -f /opt/hadoop/logs/*.log