from api.chesssite.chessapp.mysqs import MySQS
import time

q = MySQS("chessdynamics-queue")
print(q.get_queue_url())
q.send_message({"message": "hello from consumer"})
q.send_message({"message": "this message is from the consumer"})
q.send_message({"message": "goodbye from consumer"})
time.sleep(5)

while True:
    val = q.receive_message()
    if val != None:
        print(val)
