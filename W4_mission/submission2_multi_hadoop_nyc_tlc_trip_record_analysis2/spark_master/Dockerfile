FROM spark_nodebase

# Copy the master script
COPY master_entrypoint.sh $SPARK_HOME/master_entrypoint.sh
RUN chmod +x $SPARK_HOME/master_entrypoint.sh

COPY shell_files/* /root
COPY mission2.ipynb /root

# Set environment variables
EXPOSE 8080 7077 8888

CMD $SPARK_HOME/master_entrypoint.sh