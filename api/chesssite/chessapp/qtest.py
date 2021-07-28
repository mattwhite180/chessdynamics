from mysqs import MySQS
import time

q = MySQS("chessdynamics-queue")
print(q.get_queue_url())
message = {
    "function": "create",
    "game" : {
        "name" : "new qtest",
        "description" : "I WAS ALSO CREATED FROM QTEST",
        "white" : "leela3",
        # "id" : "100"
    }
}
q.send_message(message)
print(message)
