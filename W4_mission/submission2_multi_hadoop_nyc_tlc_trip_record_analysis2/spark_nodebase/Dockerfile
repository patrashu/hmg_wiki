FROM spark_base

ENV PYARROW_IGNORE_TIMEZONE=1
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install pandas pyarrow pyspark matplotlib jupyter && \
    pip3 install numpy==1.24.0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["bash"]
