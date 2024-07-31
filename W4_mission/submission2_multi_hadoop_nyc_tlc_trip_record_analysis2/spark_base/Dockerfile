FROM python:3.10-bullseye

# Set Spark ENV
ENV SPARK_VERSION=3.4.3
ENV SPARK_HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV SPARK_MASTER_HOST=spark-master
ENV PYSPARK_PYTHON=python3
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# Set Hadoop ENV
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV HDFS_NAMENODE_DIR=/opt/hadoop/hdfs/namenode
ENV HDFS_DATANODE_DIR=/opt/hadoop/hdfs/datanode
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV YARN_CONF_DIR=$HADOOP_HOME/etc/hadoop

# Install dependencies and Python, Java
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk curl vim ssh openssh-server openssh-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make Spark / Hadoop directory
RUN mkdir -p $SPARK_HOME
RUN mkdir -p $HADOOP_HOME
WORKDIR /root

# Install Spark with Hadoop Version
RUN curl -L -o /tmp/spark.tgz https://downloads.apache.org/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$SPARK_HADOOP_VERSION.tgz && \
    tar -xvzf /tmp/spark.tgz -C /opt && \
    mv /opt/spark-$SPARK_VERSION-bin-hadoop$SPARK_HADOOP_VERSION/* $SPARK_HOME && \
    rm /tmp/spark.tgz && \
    rm -rf /opt/spark-$SPARK_VERSION-bin-hadoop$SPARK_HADOOP_VERSION

# Install Hadoop
RUN curl -o /tmp/hadoop-$HADOOP_VERSION.tar.gz https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C /opt && \
    mv /opt/hadoop-$HADOOP_VERSION/* $HADOOP_HOME && \
    rm /tmp/hadoop-$HADOOP_VERSION.tar.gz && \
    rm -rf /opt/hadoop-$HADOOP_VERSION

# Grant execute permissions to the owner
RUN chmod u+x $SPARK_HOME/sbin/* && \
    chmod u+x $SPARK_HOME/bin/*

# Make log directory for Spark History Server
RUN mkdir -p $SPARK_HOME/logs && \
    chmod -R 777 $SPARK_HOME/logs

# Make HDFS directory
RUN mkdir -p $HADOOP_HOME/logs && \
    mkdir -p $HDFS_NAMENODE_DIR && \
    mkdir -p $HDFS_DATANODE_DIR && \
    chmod -R 777 $HDFS_DATANODE_DIR && \
    chmod -R 777 $HDFS_NAMENODE_DIR

# Set Spark Env
COPY spark-defaults.conf "$SPARK_HOME/conf"
COPY spark-env.sh "$SPARK_HOME/conf"
RUN echo "export JAVA_HOME=$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')" >> $SPARK_HOME/conf/spark-env.sh

# Set Hadoop Env
COPY hadoop-env.sh $HADOOP_HOME/etc/hadoop/
COPY config/* $HADOOP_HOME/etc/hadoop/

# ssh without key
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

COPY ssh_config /root/.ssh/config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Create alias for pyspark and spark-shell
RUN echo "alias pyspark='$SPARK_HOME/bin/pyspark'" >> ~/.bashrc && \
    echo "alias spark-shell='$SPARK_HOME/bin/spark-shell'" >> ~/.bashrc

EXPOSE 9864 9870 8088 9000

CMD ["bash"]
