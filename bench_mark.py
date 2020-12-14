import json
from myjson.convertor import parse
from functools import wraps
from time import perf_counter


def time_func(func):
    NUM_ITERATIONS = 10000

    @wraps(func)
    def wrapper(*args, **kwargs):
        times = []
        start = perf_counter()
        for i in range(NUM_ITERATIONS):
            ret = func(*args, **kwargs)
        end = perf_counter()
        return end- start
    return wrapper


def get_sample_json():
    val = {"name": "Ramasubramanian", "age": 28, "salaried": True,
           "score": 4.6, "others": None }
    return json.dumps(val, indent=4)


@time_func
def test_std_json(json_str):
    return json.loads(json_str)


@time_func
def test_my_json(json_str):
    return parse(json_str)


def main():
    sample_str = get_sample_json()
    t1 = test_std_json(sample_str)
    print(f"Time taken by standard parser: {t1}")
    t2 = test_my_json(sample_str)
    print(f"Time taken by my parser: {t2}")

    greater, lesser = max(t1, t2), min(t1, t2)
    times = greater // lesser
    print(f"Performance difference: {times}")


if __name__ == '__main__':
    main()