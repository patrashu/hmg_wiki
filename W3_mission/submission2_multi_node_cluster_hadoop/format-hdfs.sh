#!/bin/bash

# 환경 변수 설정
export HADOOP_HOME=/opt/hadoop
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HADOOP_HOME/lib/native

# ssh 서비스 시작
service ssh start

# HDFS 포맷 및 서비스 시작 (Master 노드에서만 실행)
if [[ $HOSTNAME == "hadoop-master" ]] && [ ! -d "$HADOOP_HOME/hdfs/namenode/current" ]; then
  hdfs namenode -format -force -nonInteractive
  touch /hdfs-formatted
fi

if [[ $HOSTNAME == "hadoop-master" ]]; then
  $HADOOP_HOME/sbin/start-dfs.sh
  $HADOOP_HOME/bin/yarn --daemon start resourcemanager
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
else
  $HADOOP_HOME/bin/hadoop --daemon start datanode
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
fi

# 로그 파일을 출력하여 컨테이너 실행 유지
tail -f /dev/null
