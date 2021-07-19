from api.chesssite.chessapp.mysqs import MySQS                                                                

q = MySQS('mattw-chessdynamics-test.fifo')
print(q.get_queue_url())
print("messages:", q.count())
q.send_message("hello from consumer")
print("messages:", q.count())
print(q.receive_message())
print("messages:", q.count())
