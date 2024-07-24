from argparse import ArgumentParser

import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import NumericType, TimestampNTZType


def merge_data(spark: SparkSession, output_dir: str, start_date: str, end_date: str):
    sy, sm = start_date.split('-')
    ey, em = end_date.split('-')
    tmp_df = []
    for year in range(int(sy), int(ey)+1):
        for month in range(1, 13):
            if year == int(sy) and month < int(sm):
                continue
            if year == int(ey) and month > int(em):
                continue
            file_path = f'{output_dir}/fhvhv_tripdata_{year}-{str(month).zfill(2)}.parquet'
            tmp_df.append(spark.read.parquet(file_path))

    if len(tmp_df) == 1:
        return tmp_df[0]
    return tmp_df[0].union(*tmp_df[1:])


def remove_missing_values(df):
    return df.na.drop()


def fill_missing_values(df):
    # mode_value = df.groupBy(col).count().orderBy($"count".desc).first()[0] # spark-shell
    for col in df.columns:
        try:
            mode_value = df.groupBy(col).count().orderBy(
                F.col("count").desc()).first()[0]
            df = df.na.fill({col: mode_value})
        except:
            df = df.na.drop(subset=[col])
    return df


def preprocess_msvalue(df, method: str):
    if method == 'remove':
        return remove_missing_values(df)
    elif method == 'fill':
        return fill_missing_values(df)
    else:
        raise ValueError(f"Unknown method: {method}")


def convert_time_to_timestamp(df):
    for col in df.columns:
        dtype = df.schema[col].dataType
        if isinstance(dtype, TimestampNTZType):
            df = df.withColumn(col, F.date_format(
                col, 'yyyy-MM-dd HH:mm:ss'))

    return df


def remove_invalid_values(df):
    for col in df.columns:
        if isinstance(df.schema[col].dataType, NumericType):
            df = df.withColumn(col, F.when(
                F.col(col) >= 0, F.col(col)).otherwise(None))
            df = df.na.drop(subset=[col])
    return df


def calculate_trip_avg_duration(df):
    avg_trip_time = df.select(F.avg(F.col("trip_time").cast(
        "long")).alias("avg_trip_time")).collect()[0][0]
    # avg_time_df = df.groupBy('trip_time').agg(F.avg('trip_duration').alias('trip_avg_duration'))
    return avg_trip_time


def calculate_trip_avg_distance(df):
    avg_dist_time = df.select(F.avg(F.col("trip_miles").cast(
        "long")).alias("avg_trip_dist")).collect()[0][0]
    return avg_dist_time


def calculate_peak_hours(df):
    df = df.withColumn("hour", F.hour("pickup_datetime")
                       )  # extract hour from timestamp
    hourly_trips = df.groupBy("hour").count().orderBy("hour")
    hourly_trips_df = hourly_trips.toPandas()
    return hourly_trips_df


if __name__ == '__main__':
    spark = SparkSession.builder \
        .appName("NYC Taxi Data Analysis") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    parser = ArgumentParser()
    parser.add_argument(
        "--output_dir", default='hdfs://hadoop-single:9000/data', type=str)
    parser.add_argument(
        "--save_dir", default='hdfs://hadoop-single:9000/results', type=str)
    parser.add_argument(
        '--start_date', default='2023-01', type=str)
    parser.add_argument(
        '--end_date', default='2023-01', type=str)
    args = parser.parse_args()

    # 데이터 병합
    total_df = merge_data(spark, args.output_dir,
                          args.start_date, args.end_date)

    print("Total data count: ", total_df.count())
    # 누락된 값 제거 / 변환
    df = preprocess_msvalue(total_df, "remove")

    # 시간을 timestamp로 변환
    df = convert_time_to_timestamp(df)

    # 말도 안되는 값을 가진 row제거
    df = remove_invalid_values(df)
    df = preprocess_msvalue(df, 'remove')
    print("Preprocessed data count: ", df.count())

    # 평균 여행 시간/ 거리 계산
    avg_time = calculate_trip_avg_duration(df)
    avg_dist = calculate_trip_avg_distance(df)

    print("Average trip time:", round(avg_time, 2), "seconds")
    print("Average trip distance:", round(avg_dist, 2), "miles")

    # 피크 시간 계산
    hourly_trips_df = calculate_peak_hours(df)
    plt.figure(figsize=(10, 6))
    plt.bar(hourly_trips_df['hour'], hourly_trips_df['count'], color='skyblue')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Trips')
    plt.title('Distribution of Trips Across Different Hours of the Day')
    plt.xticks(range(0, 24))
    plt.grid(axis='y')

    peak_hours = hourly_trips_df[hourly_trips_df['count']
                                 == hourly_trips_df['count'].max()]['hour']
    for peak_hour in peak_hours:
        plt.gca().patches[peak_hour].set_color('orange')

    # local에 결과 저장
    plt.tight_layout()
    plt.savefig(f"peak_hours.png")

    # # 전처리된 데이터 저장
    # preprocessed_data_path = f"{args.save_dir}"

    # # 전처리된 데이터 저장을 위한 HDFS 명령어 실행
    # df.write.csv(args.save_dir, header=True, mode='overwrite')

    spark.stop()
