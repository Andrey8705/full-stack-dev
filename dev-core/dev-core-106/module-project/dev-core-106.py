hello = "Hello, World!"

def say_hello():
    print(hello)

say_hello()

user_input = input("1 or 2?")
if user_input == "1":
    say_hello()
else:
    print("Goodbye!")