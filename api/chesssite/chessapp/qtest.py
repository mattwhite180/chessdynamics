from mysqs import MySQS
import time

q = MySQS("chessdynamics-queue")
print(q.get_queue_url())
message = {
    "function": "create",
    "game" : {
        "name" : "QTEST",
        "description" : "I WAS CREATED FROM QTEST",
        "white" : "leela2",
        # "id" : "100"
    }
}
q.send_message(message)
print(message)
