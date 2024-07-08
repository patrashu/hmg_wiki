from multiprocessing import Queue


"""
Put() function is used to push an item to the queue.
Get() function is used to pop an item from the queue.
"""


if __name__ == '__main__':
    items = ['red', 'green', 'blue', 'black']
    queue = Queue()
    counter = 1
    print("pushing items to queue:")

    for item in items:
        print(f"item no: {counter} {item}")
        queue.put([counter, item])
        counter += 1

    print("popping items from queue:")
    while not queue.empty():
        num, item = queue.get()
        print(f"item no: {num} {item}")
