import os
import shutil
import xml.etree.ElementTree as ET

HADOOP_CONF_DIR = "/opt/hadoop/etc/hadoop"


# python에서 백업파일은 명시적으로 .bak 표기를 진행함.
def backup_file(filename: str) -> None:
    print("Backing up", filename, '...')
    _filepath = os.path.join(HADOOP_CONF_DIR, filename)
    shutil.copy(_filepath, _filepath + '.bak')
    assert os.path.exists(_filepath + '.bak')


def modify_config_file(filename: str, modifications: dict) -> None:
    _filepath = os.path.join(HADOOP_CONF_DIR, filename)
    tree = ET.parse(_filepath)
    root = tree.getroot()

    for name, value in modifications.items():
        for prop in root.findall('property'):
            if prop.find('name').text == name:
                prop.find('value').text = value

    tree.write(_filepath)


def run():
    core_site_modifications = {
        "fs.defaultFS": "hdfs://namenode:9000",
        "hadoop.tmp.dir": "/hadoop/tmp",
        "io.file.buffer.size": "131072"
    }

    hdfs_site_modifications = {
        "dfs.replication": "2",
        "dfs.blocksize": "134217728",
        "dfs.namenode.name.dir": "/hadoop/dfs/name"
    }

    mapred_site_modifications = {
        "mapreduce.framework.name": "yarn",
        "mapreduce.jobhistory.address": "namenode:10020",
        "mapreduce.task.io.sort.mb": "256"
    }

    yarn_site_modifications = {
        "yarn.resourcemanager.hostname": "namenode",
        "yarn.resourcemanager.address": "namenode:8032",
        "yarn.nodemanager.resource.memory-mb": "8192",
        "yarn.scheduler.minimum-allocation-mb": "1024"
    }

    modify_configs_dict = {
        "core-site.xml": core_site_modifications,
        "hdfs-site.xml": hdfs_site_modifications,
        "mapred-site.xml": mapred_site_modifications,
        "yarn-site.xml": yarn_site_modifications
    }

    try:
        for config_filename, modify_dict in modify_configs_dict.items():
            backup_file(config_filename)
            modify_config_file(config_filename, modify_dict)
    except Exception as e:
        print("An error occurred:", e)
    else:
        print("Stopping Hadoop DFS ...")
        os.system("/opt/hadoop/sbin/stop-dfs.sh")
        print("Stopping YARN ...")
        os.system("/opt/hadoop/sbin/stop-yarn.sh")
        os.system("rm -rf /hadoop/dfs/name")
        print("Starting Hadoop DFS ...")
        os.system("/opt/hadoop/sbin/start-dfs.sh")
        print("Starting YARN ...")
        os.system("/opt/hadoop/sbin/start-yarn.sh")
        print("Configuration changes applied and services restarted.")


if __name__ == '__main__':
    run()
