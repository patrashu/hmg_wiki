from multiprocessing import Process
import time


def print_continent(continent: str = "Asia"):
    print(f'The name of continent is {continent}')


"""
start() 함수는 생성한 프로세스 인스턴스들을 실행시키는 함수이다.
join() 함수는 생성한 프로세스 인스턴스들이 모두 종료될 때까지 기다리는 함수이다.
하나의 스크립트 파일 내에서 실행한 인스턴스들이 종료되기를 기다리기 위해 join() 함수를 사용한다.
"""

if __name__ == '__main__':
    names = ["America", "Europe", "Africa"]
    processes = []
    process = Process(target=print_continent)

    for name in names:
        process = Process(target=print_continent, args=(name,))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()
