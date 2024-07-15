export HDFS_NAMENODE_USER=hdfs
export HDFS_DATANODE_USER=hdfs
export HDFS_SECONDARYNAMENODE_USER=hdfs
export YARN_RESOURCEMANAGER_USER=yarn
export YARN_NODEMANAGER_USER=yarn

# Ensure Hadoop binaries are in PATH
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

if [ -d "$HDFS_NAMENODE_DIR/current" ]; then
  echo "HDFS is already formatted."
else
  echo "Formatting HDFS..."
  yes Y | hdfs namenode -format -force -nonInteractive
fi

start-dfs.sh
start-yarn.sh

# Keep the container running
while true; do sleep 1000; done