import inspect


def log(o):
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)

    print("-------------------------------")
    print("🐛", f"[{calframe[1][1].split('primordialPanda')[1][1:]}]", o)
    print("-------------------------------")
