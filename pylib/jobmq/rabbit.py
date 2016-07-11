"""
RabbitMQ job pipe
"""

import pika
import signal
import time

class JobMQ:
  def __init__(server_addr,q):
    conn    = pika.BlockingConnection(pika.ConnectionParameters(server_addr))
    channel = conn.channel()
    channel.queue_declare(queue=q)

    self.conn    = conn
    self.channel = channel
    self.q_name  = q

  def publish(job):
    self.channel.basic_publish(
      exchange='',
      routing_key=self.q_name,
      body=job)

  def next():
    pass

  # Message generator
def iter(transformation=lambda x:x):
  TIMEOUT = 5 # seconds
  # Start the awaiting signal
  try:
    def __timeout(signum,frame):
      raise StopIteration

    signal.signal(signal.SIGALRM,__timeout)
    signal.alarm(TIMEOUT)
    for methodframe, prop, body in self.channel.consume(self.q_name):
      signal.alarm(0)
      job = transformation(body.decode('utf-8'))
      
      yield job
      self.channel.basic_ack(methodframe.delivery_tag)
      
      # Startover a new timer
      signal.alarm(TIMEOUT)

  except StopIteration as e:
    signal.alarm(0) # Cancel the timer
    print(colored('--Timeout, no further message--','yellow'))
    raise
  except Exception as e:
    signal.alarm(0) 
    print(colored('--Exception broke the iteration--','yellow'))
    raise

def end():
  print('Ending MQ # ',self.q_name)
  try:
    self.conn.close()
  except pika.exceptions.ConnectionClosed:
    print(colored('MQ appeared offline','red'))

