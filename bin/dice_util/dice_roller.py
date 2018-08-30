from random import randrange


def roll_xdy(x, y):
    nums = list()
    sum = 0
    for i in range(x):
        nums.append(randrange(y)+1)
        sum += nums[-1]
    return (sum, nums)