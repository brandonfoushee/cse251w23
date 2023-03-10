import os
import random
import sys
import threading
import time
from datetime import datetime, timedelta

# Global Consts
SLEEP_REDUCE_FACTOR = 5000
FOOD_TO_MAKE = 100

global size_of_table


class Food:

    kind = ('Apple', 'Chocolate', 'Sugar', 'Bacon', 'Bread', 'Strawberry', 'Orange', 'Banana',
            'Celery', 'Beef', 'Chicken', 'Peanut Butter')

    def __init__(self):
        self.choice = random.choice(Food.kind)

        # Takes some time to prepare food
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        #print(f'putting {self.choice} on the table')

    def __str__(self) -> str:
        return self.choice


class Queue251():

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Feeder(threading.Thread):
    def __init__(self,
                 feeder_index,
                 sem_mouth_full: threading.Semaphore,
                 sem_can_I_eat: threading.Semaphore,
                 table_queue,
                 table_lock,
                 number_of_eaters):

        threading.Thread.__init__(self)
        self.feeder_index = feeder_index
        self.sem_mouth_full = sem_mouth_full
        self.sem_can_I_eat = sem_can_I_eat
        self.table_queue = table_queue
        self.table_lock = table_lock
        self.number_of_eaters = number_of_eaters
        self.food_made = 0

    def run(self):
        global size_of_table

        for _ in range(FOOD_TO_MAKE):

            # If the eater's mouth is full, then wait for him/her to eat and digest
            self.sem_mouth_full.acquire()

            # Put some food on the table, lock to ensure another feeder/eater doesn't
            # try and put/eat food at the same time
            self.table_lock.acquire()
            self.table_queue.put(Food())
            self.food_made += 1
            self.table_lock.release()

            # Tell the eater that I put food on the table and he/she can eat
            self.sem_can_I_eat.release()

        # "Wake up/signal" the eater one more time that all food is done.
        # If using multiple eaters (threads), then use a loop to put enough 'None' objects
        # on the table to ensure all threads could pop off their own 'None' object.
        # (don't use a global, you'll need to pass in the number of eaters)
        if(self.feeder_index == 0):
            for _ in range(self.number_of_eaters):
                self.sem_mouth_full.acquire()
                self.table_lock.acquire()
                self.table_queue.put(None)
                self.table_lock.release()

                # This tells the eater to "eat" the None object and not block on acquire,
                # needs to be after putting None on the queue
                self.sem_can_I_eat.release()


class Eater(threading.Thread):

    def __init__(self,
                 eater_index,
                 sem_mouth_full: threading.Semaphore,
                 sem_can_I_eat: threading.Semaphore,
                 table_queue,
                 table_lock):

        threading.Thread.__init__(self)
        self.eater_index = eater_index
        self.sem_mouth_full = sem_mouth_full
        self.sem_can_I_eat = sem_can_I_eat
        self.table_queue = table_queue
        self.table_lock = table_lock
        self.food_eaten = 0

    def run(self):
        while True:

            # Wait for food to be made before I can eat
            self.sem_can_I_eat.acquire()

            # Let's eat!
            # Put some food on the table, lock to ensure another feeder/eater doesn't
            # try and put/eat food at the same time
            self.table_lock.acquire()
            food = self.table_queue.get()
            #print(f'eating {food}')
            self.table_lock.release()

            # are we done?
            if(food == None):
                #print(f'thread {self} is done eating')
                break

            # I took one item off the table and ate it
            self.food_eaten += 1

            # I ate one, so mouth has more room (increment counter by 1).
            # If count is zero (before incrementing), then tell feeder to make more food
            self.sem_mouth_full.release()

            # Need some time to digest
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))


def main(number_of_eaters, number_of_feeders):

    print(
        f'\n### Starting with {number_of_eaters} eater(s) and {number_of_feeders} feeder(s) ###\n')

    # An eater can hold 'n' things in their mouth. An eater will eat whenever there
    # is anything on the table. So, we need to limit the size of the table to what
    # an eater can hold in their mouth (so they don't break their jaw?).
    size_of_table = random.randint(5, 15)

    # When count goes down to 0, then eater can't put any more into their mouth, so
    # tell the feeders, through a semaphore, to wait (i.e., block) until eater can chew
    # and digest.
    sem_mouth_full = threading.Semaphore(size_of_table)

    # Binary choice: is there food for me to eat? Initially, no, so set count to zero
    # so eater will wait for food to get made
    sem_can_I_eat = threading.Semaphore(0)

    # Create a place to put food, a table
    table_queue = Queue251()

    # A lock to prevent someone from trying to eat when nothing is on it
    # (i.e., calling pop when list is empty), and prevent race condition
    # between eaters and feeders.
    table_lock = threading.Lock()

    # create feeders
    feeders = []
    for feader_index in range(number_of_feeders):
        feeders.append(
            Feeder(feader_index, sem_mouth_full, sem_can_I_eat, table_queue, table_lock, number_of_eaters))

    # create eaters
    eaters = []
    for eater_index in range(number_of_eaters):
        eaters.append(Eater(eater_index, sem_mouth_full, sem_can_I_eat,
                      table_queue, table_lock))

    # start feeders
    for feeder in feeders:
        feeder.start()

    # start eaters
    for eater in eaters:
        eater.start()

    # wait for feeders to be done
    for feeder in feeders:
        feeder.join()

    # wait for eaters to be done
    for eater in eaters:
        eater.join()

    print(f'Maximum number of food on table = {table_queue.get_max_size()}')
    assert table_queue.get_max_size(
    ) <= size_of_table, f'table max size is {table_queue.get_max_size()} but should be less than or equal to {size_of_table}'

    eaten = 0
    made = 0
    for feeder in feeders:
        made += feeder.food_made
    for eater in eaters:
        eaten += eater.food_eaten

    print(f'Total amount of food made = {made}')
    print(f'Total amount of food eaten = {eaten}')

    assert made == eaten, f'Total amount of food made is {made}, which does not equal amount of food eaten of {eaten}'


if __name__ == '__main__':
    main(1, 1)
    print('Exiting program')
