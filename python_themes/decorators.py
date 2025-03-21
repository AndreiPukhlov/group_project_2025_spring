# @fancy_decorator

def fancy_decorator(func):
    def wrapper():
        print("✨ Fancy Start ✨")
        print("✨" * 8)
        func()
        print("✨" * 8)
        print("✨ Fancy End ✨")

    return wrapper

@fancy_decorator
def add():
    print(f"    Result is: {1 + 12}")


def say_hello():
    print("Hello!")


def say_hi():
    print('Hi!')


def say_hey():
    print("Hey!")


# say_hi()
# print()
# say_hey()
# print()
# say_hello()
# print()
add()
