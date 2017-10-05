import simpy
import numpy
from constants import *
from transaction import *

queue_1_lengths = []
queue_1_waiting_time = []
queue_1_service_time = []

queue_2_lengths = []
queue_2_waiting_time = []
queue_2_service_time = []

queue_3_lengths = []
queue_3_waiting_time = []
queue_3_service_time = []


class Transaction(object):
    def __init__(self, env, name, system):
        self.name = name
        self.env = env
        self.system = system

    def run(self):

        global queue_1_len, queue_2_len, queue_3_len
        global leave_2, leave_3

        queue_1_len += 1
        creation_time = self.env.now

        with self.system.request() as request_1:
            yield request_1

            queue_1_len -= 1

            wait = self.env.now - creation_time
            queue_1_waiting_time.append(self.env.now - creation_time)
            queue_1_lengths.append(queue_1_len)

            service_duration = numpy.random.exponential(MB)
            yield self.env.timeout(service_duration)

            queue_1_service_time.append(self.env.now - creation_time)

            print(u"FIRST - name: {0} - serving: {1} - waiting: {2}".format(
                self.name, self.env.now - creation_time, wait))

            if numpy.random.randint(1, 1000) > (Q * 1000):
                #smo3
                if queue_3_len == E3:
                    print("poka from3 my name is{}".format(self.name))
                    leave_3 += 1
                    return

                queue_3_len += 1
                queue_3_comes_time = self.env.now
                self.system = system_3
                with self.system.request() as request_3:
                    yield request_3

                    queue_3_len -= 1
                    wait = self.env.now - queue_3_comes_time
                    queue_3_waiting_time.append(self.env.now - queue_3_comes_time)
                    queue_3_lengths.append(queue_3_len)

                    service_duration = numpy.random.exponential(MB)
                    yield self.env.timeout(service_duration)

                    queue_3_service_time.append(self.env.now - queue_3_comes_time)
                    print(u"THIRD - name: {0} - serving: {1} - waiting: {2}".format(
                        self.name, self.env.now - queue_3_comes_time, wait))
            else:
                # smo2
                if queue_2_len == E2:
                    print("poka from2 my name is{}".format(self.name))
                    leave_2 += 1
                    return

                queue_2_len += 1
                queue_2_comes_time = self.env.now
                self.system = system_2
                with self.system.request() as request_2:
                    yield request_2

                    queue_2_len -= 1
                    wait = self.env.now - queue_2_comes_time
                    queue_2_waiting_time.append(self.env.now - queue_2_comes_time)
                    queue_2_lengths.append(queue_2_len)

                    service_duration = numpy.random.exponential(MB)
                    yield self.env.timeout(service_duration)

                    queue_2_service_time.append(self.env.now - queue_2_comes_time)
                    print(u"SECOND - name: {0} - serving: {1} - waiting: {2}".format(
                        self.name, self.env.now - queue_2_comes_time, wait))
        print(leave_2, leave_3)
