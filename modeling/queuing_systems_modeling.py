from numpy import mean, minimum, std
from transaction import *


def calculate():
    env.process(generate())
    env.run()

    p_lost_2 = calculate_probability_of_losing(constants.lost_2, len(system_2_transactions_intervals))
    p_lost_3 = calculate_probability_of_losing(constants.lost_3, len(system_3_transactions_intervals))

    zagr1 = calculate_loading(system_1_service_duration, system_1_transactions_intervals, k=K)
    zagr2 = calculate_loading(system_2_service_duration, system_2_transactions_intervals, p=p_lost_2)
    zagr3 = calculate_loading(system_3_service_duration, system_3_transactions_intervals, p=p_lost_3)

    nagr1 = calculate_loading(system_1_service_duration, system_1_transactions_intervals, max=K)
    nagr2 = calculate_loading(system_2_service_duration, system_2_transactions_intervals)
    nagr3 = calculate_loading(system_3_service_duration, system_3_transactions_intervals)

    ozhid1 = mean(queue_1_waiting_time)
    ozhid2 = mean(queue_2_waiting_time)
    ozhid3 = mean(queue_3_waiting_time)

    dlina1 = mean(queue_1_length)
    dlina2 = mean(queue_2_length)
    dlina3 = mean(queue_3_length)

    prebyvanie1 = mean(system_1_service_duration) + mean(queue_1_waiting_time)
    prebyvanie2 = mean(system_2_service_duration) + mean(queue_2_waiting_time)
    prebyvanie3 = mean(system_3_service_duration) + mean(queue_3_waiting_time)

    lifecycle = mean(global_time)
    varcoef = std(global_time) / mean(global_time)

    # print("\nzagr1 = ", zagr1)
    # print("zagr2 = ", zagr2)
    # print("zagr3 = ", zagr3)
    #
    # print("\nnagr1 = ", nagr1)
    # print("nagr2 = ", nagr2)
    # print("nagr3 = ", nagr3)
    #
    # print("\nozhid1 = ", ozhid1)
    # print("ozhid2 = ", ozhid2)
    # print("ozhid3 = ", ozhid3)
    #
    # print("\ndlina1 = ", dlina1)
    # print("dlina2 = ", dlina2)
    # print("dlina3 = ", dlina3)
    #
    # print("\nprebyvanie1 = ", prebyvanie1)
    # print("prebyvanie2 = ", prebyvanie2)
    # print("prebyvanie3 = ", prebyvanie3)
    #
    # print("\nlifecycle = ", lifecycle)
    # print("varcoef = ", varcoef)
    #
    # print("\nlost2 = ", p_lost_2)
    # print("lost3 = ", p_lost_3)

    return (
        zagr1, zagr2, zagr3,
        nagr1, nagr2, nagr3,
        ozhid1, ozhid2, ozhid3,
        dlina1, dlina2, dlina3,
        prebyvanie1, prebyvanie2, prebyvanie3,
        lifecycle, varcoef,
        p_lost_2, p_lost_3
    )


def generate():
    transaction_cnt = 0
    while transaction_cnt < TRANSACTIONS_NUMBER:
        transaction_cnt += 1
        interval = numpy.random.exponential(1/LAMBDA)
        system_1_transactions_intervals.append(interval)
        yield env.timeout(interval)

        env.process(Transaction.run())


def calculate_loading(array_b, array_intervals, max=1, k=1, p=0):
    b = mean(array_b)
    lyambda = 1 / mean(array_intervals)
    return minimum((1 - p) * b * lyambda / k, max)


def calculate_probability_of_losing(lost, element_number):
    return lost / element_number
