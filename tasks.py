from celery import Celery
import socketio
import os
import random
import time


# Initialize Celery
config={}
config['CELERY_BROKER_URL']  = 'amqp://guest:guest@localhost:5672/'
config['CELERY_RESULT_BACKEND'] = 'amqp://guest:guest@localhost:5672/'
celery = Celery('tasks', broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)

# connect to the RabbitMQ queue through Kombu
rabbitMq = socketio.KombuManager('amqp://', write_only = True)
# now, it is ready to emit the message as
# rabbitMq.emit('title', {'data', 'data here'}, namespace='/test')


@celery.task
def long_task():
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.5:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        meta = {'current': i, 'total': total, 'status': message}
        time.sleep(0.5)
        if random.random() < 0.5 :
            rabbitMq.emit('my response', {'data': message},
                     namespace='/test')
    rabbitMq.emit('my response', {'data': "long_task completed."},
                     namespace='/test')
    
@celery.task
def add(x, y):
    return x + y