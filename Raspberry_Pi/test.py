from queue import Queue
from threading import Condition, Thread

condition = True

# create a data producer 
def producer(output_queue):
    global condition
    while condition:
        data = "Hello world"
        #print("T1: ")
        output_queue.put(data)
        

# create a consumer
def consumer(input_queue):
    global condition
    while condition:
        data = input_queue.get()
        #print("T2: " + data)
        input_queue.task_done()

   #input_queue.put("Test")

def printOut(input_queue):
    global condition
    print("T3: ")
    print (input_queue.empty())

    string = str(input())
    print(string)
    condition = False
  

    #data = input_queue.get()
    #print("T2: " + data)
    #input_queue.task_done()
    
        

q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t3 = Thread(target=printOut, args=(q,))
t1.start()
t2.start()
t3.start()