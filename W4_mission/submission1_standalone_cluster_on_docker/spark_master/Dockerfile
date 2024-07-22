FROM spark_base

# Copy the master script
COPY master_entrypoint.sh $SPARK_HOME/master_entrypoint.sh
RUN chmod +x $SPARK_HOME/master_entrypoint.sh

# Set environment variables
EXPOSE 8080 7077 4040

CMD $SPARK_HOME/master_entrypoint.sh