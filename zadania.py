import math

# 5


def find_divisible_by_3() -> int:
    divisible: list[int] = [x for x in range(101) if x % 3 == 0 and x != 0]
    return len(divisible)


print(f'Divisible by 3 in 0-100: {find_divisible_by_3()}')


# 6
def find_divisible_by_n(a: int, n: int) -> int:
    divisible: list[int] = [x for x in range(n+1) if x % a == 0 and x != 0]
    return len(divisible)


print(f'Divisible by 4 in 0-20: {find_divisible_by_n(4, 20)}')


# 7
test_arr: list[float] = [2314, 45634, 341, 3578, 234253, 12,
                         3, 12, 4, 34, 6, 54, 7, 43, 5, 233,
                         23, 36, 87, 56, 789, 567, 9, 57, 789]

max_: float = -math.inf
for a in test_arr:
    if a > max_:
        max_ = a
print(f'Max value: {max_}')


# 8
# O(n)
def find_max(arr: list[float]) -> float:
    max_: float = -math.inf
    for a in arr:
        if a > max_:
            max_ = a
    return max_


print(f'Max value: {find_max(test_arr)}')


# 9
def foo9(x: float, a: float, b: float, c: float) -> float:
    return a*x**2 + b*x + c


print(f'Value: {foo9(10, 4.5, 23, 11)}')
