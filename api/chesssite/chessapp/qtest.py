from mysqs import MySQS
import time

q = MySQS("chessdynamics-queue")
print(q.get_queue_url())
message = {
    "function": "delete",
    "game" : {
        "name" : "this is the create test",
        "description" : "this is the description",
        "white" : "white player",
        "id" : "90"
    }
}
q.send_message(message)
print(message)
