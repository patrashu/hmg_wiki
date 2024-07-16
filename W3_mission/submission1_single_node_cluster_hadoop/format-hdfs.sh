
# HDFS 포맷 (첫 실행 시에만 필요)
if [ ! -d "/opt/hadoop/hdfs/namenode/current" ]; then
  echo "Formatting HDFS namenode..."
  /opt/hadoop/bin/hdfs namenode -format -force -nonInteractive
fi

echo "Starting HDFS namenode..."
/opt/hadoop/sbin/hadoop-daemon.sh start namenode

echo "Starting HDFS datanode..."
/opt/hadoop/sbin/hadoop-daemon.sh start datanode

echo "Starting YARN resource manager..."
/opt/hadoop/sbin/yarn-daemon.sh start resourcemanager

echo "Starting YARN node manager..."
/opt/hadoop/sbin/yarn-daemon.sh start nodemanager

echo "Starting HDFS secondary namenode..."
/opt/hadoop/sbin/hadoop-daemon.sh start secondarynamenode

tail -f /opt/hadoop/logs/*.log

/usr/sbin/sshd -D