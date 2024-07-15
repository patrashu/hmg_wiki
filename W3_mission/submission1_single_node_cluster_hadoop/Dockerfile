# Base image
FROM openjdk:8-jdk-slim

# Set environment variables
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_HOME /opt/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin
ENV HDFS_NAMENODE_DIR /opt/hadoop/hdfs/namenode
ENV HDFS_DATANODE_DIR /opt/hadoop/hdfs/datanode

# Install necessary packages
RUN apt-get update -y && \
    apt-get install -y wget sudo curl ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create hdfs and yarn users
RUN useradd -ms /bin/bash hdfs && \
    useradd -ms /bin/bash yarn

# Download and install Hadoop
RUN curl -o /tmp/hadoop-$HADOOP_VERSION.tar.gz https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C /opt/ && \
    mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm /tmp/hadoop-$HADOOP_VERSION.tar.gz && \
    chown -R hdfs:hdfs $HADOOP_HOME && \
    chown -R yarn:yarn $HADOOP_HOME

# Copy configuration files
COPY core-site.xml $HADOOP_HOME/etc/hadoop/
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/
COPY mapred-site.xml $HADOOP_HOME/etc/hadoop/
COPY yarn-site.xml $HADOOP_HOME/etc/hadoop/

# Make HDFS directories and set permissions
RUN mkdir -p /opt/hadoop/hdfs/namenode && \
    mkdir -p /opt/hadoop/hdfs/datanode && \
    chown -R hdfs:hdfs /opt/hadoop/hdfs

# SSH setup
RUN apt-get update && apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd && \
    echo "export VISIBLE=now" >> /etc/profile

# Copy format script
COPY format-hdfs.sh /usr/local/bin/format-hdfs.sh
RUN chmod +x /usr/local/bin/format-hdfs.sh

# Expose ports
# DataNode, NameNode, NodeManager, ResourceManager's UI port, ssh
# DataNode, NameNode IPC, Sec NameNode UI, MapReduce History, NameNode RPC
EXPOSE 9864 9870 8042 8088 22
EXPOSE 9866 9867 9871 10020 8020

# restaet ssh and run the hadoop services
CMD service ssh start && su - hdfs -c "/usr/local/bin/format-hdfs.sh"

