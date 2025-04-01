# @fancy_decorator
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        result = end - start
        if result < 60:
            if result < 2:
                print(f"It takes {round(result)} second")
            else:
                print(f"It takes {round(result)} seconds")

        else:
            if result < 120:
                print(f"It takes {round(result / 60)} minute and {round(result % 60)} seconds")
            else:
                print(f"It takes {round(result / 60)} minutes and {round(result % 60)} seconds")

    return wrapper


def fancy_decorator(func):
    def wrapper(*args, **kwargs):
        print("✨ Салат ✨")
        print("✨" * 8)
        func(*args, **kwargs)
        print("✨" * 8)
        print("✨ Одна порция ✨")

    return wrapper


def seld_pod_shuboy():
    print("Сельдь под шубой")


def olivie():
    print("Оливье!")


@fancy_decorator
def mimoza():
    print('Мимоза')


def vesenniy():
    print("Весенний!")

@fancy_decorator
def salat(name):
    print(name)


def input_():
    name = input("enter name: ")
    salat(name)


#
#
# seld_pod_shuboy()
# print()
# olivie()
# print()
# vesenniy()


# print()
mimoza()
# input_()

def sleeeeep():
    time.sleep(1)

# sleeeeep()
