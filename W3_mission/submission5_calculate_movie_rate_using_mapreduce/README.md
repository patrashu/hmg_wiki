## Average Rating of Movies using MapReduce

### Funtional Requirements

- 데이터 처리
    - ~~hdfs에서 입력 데이터를 올바르게 읽어야 함~~
    - ~~Mapper는 각 레코드를 처리하고 영화 ID와 Rating에 관련된 Key-Value 값을 보내야 함~~
    - ~~Reducer는 Mapper의 Key-Value 결과를 집계하여 각 영화의 평균 평점을 계산하고 출력해야 함.~~
- 프로그램 실행
    - ~~MapReduce 작업은 Hadoop에서 오류없이 실행되어야 함.~~
    - ~~입력 데이터를 효율적으로 처리하고 정확한 결과를 생성해야 함.~~
- 결과 출력
    - ~~결과물은 HDFS에 저장된 txt 파일이어야 함.~~
    - ~~출력 파일의 각 줄에는 영화 ID와 평균 평점이 포함되어야 함.~~
    - ~~출력은 HDFS에서 검색하고 읽을 수 있어야 함.~~

### Mapper

- Python Script를 활용하여 Mapper 클래스를 구현하고, 이를 활용하여 Map 작업을 수행합니다.
- csv로 저장된 파일을 한 줄씩 읽어와 Movie ID와 Rating이 적힌 column Data를 추출합니다.

### Reducer

- Python Script를 활용하여 Reducer 클래스를 구현하고, 이를 활용하여 Reduce 작업을 수행합니다.
- Mapper의 결과를 받아와 각 감정 카테고리에 대한 총 개수를 집계합니다.

### 실행 및 결과 확인

- `hdfs dfs -put ratings.csv /movie_rate`를 통해 파일을 업로드합니다.
    
    ![스크린샷 2024-07-19 오후 5.31.01.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/4b0f9250-7789-4f57-b6d5-154ad10ea058/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2024-07-19_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_5.31.01.png)
    
- `calculate_movie_rate.sh`를 통해 MapReduce 작업을 수행합니다.
    
    ![스크린샷 2024-07-19 오후 5.36.39.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/ae345893-5dae-45f3-8b79-ce3f4b93121c/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2024-07-19_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_5.36.39.png)
    
- `hdfs dfs -ls /movie_rate_output`을 통해 2개의 partition 결과를 확인했습니다.
    
    ![스크린샷 2024-07-19 오후 5.38.14.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/851ef575-4c98-49fb-8ddf-0fdb4ae80585/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2024-07-19_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_5.38.14.png)
    
- `hdfs dfs -cat /movie_rate_output/part-00001`을 통해 결과를 확인합니다.