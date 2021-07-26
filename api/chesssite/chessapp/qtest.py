from mysqs import MySQS
import time

q = MySQS("chessdynamics-queue")
print(q.get_queue_url())
message = {"id": "57", "function": "play_move", "move": "e8d7"}
q.send_message(message)
print(message)
