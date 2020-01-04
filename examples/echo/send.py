import stomp

conn = stomp.Connection([("rabbitmq", 61613)])
conn.connect()
conn.send("/queue/echo", "howdy")
conn.send("/queue/unsubscribed", "this message is ignored")
