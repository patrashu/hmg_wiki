# rollback config

HADOOP_CONF_DIR="/opt/hadoop/etc/hadoop"

rollback_config() {
    local filename=$1
    local backup_file="${HADOOP_CONF_DIR}/${filename}.bak"
    if [[ -f "$backup_file" ]]; then
        echo "Rolling back $filename..."
        cp "$backup_file" "${HADOOP_CONF_DIR}/${filename}"
    else
        echo "Backup file not found. Cannot rollback $filename."
        exit 1
    fi
}


modify_configs_list="core-site.xml hdfs-site.xml mapred-site.xml yarn-site.xml"
for filename in $modify_configs_list; do
    rollback_config "$filename"
done

echo "Stopping Hadoop DFS..."
/opt/hadoop/sbin/stop-dfs.sh
echo "Stopping YARN..."
/opt/hadoop/sbin/stop-yarn.sh

echo "Starting Hadoop DFS..."
/opt/hadoop/sbin/start-dfs.sh
echo "Starting YARN..."
/opt/hadoop/sbin/start-yarn.sh
