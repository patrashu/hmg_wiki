FROM spark_nodebase

COPY worker_entrypoint.sh $SPARK_HOME/worker_entrypoint.sh
RUN chmod +x $SPARK_HOME/worker_entrypoint.sh

EXPOSE 8081

CMD $SPARK_HOME/worker_entrypoint.sh
