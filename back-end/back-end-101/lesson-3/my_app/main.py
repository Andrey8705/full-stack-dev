from utils.helpers import make_breakfast, brush_teeth, do_laundry, make_coffee, wash_dishes

def main():
    print("Готовим завтрак")
    make_breakfast()
    print("\n")

    print("Стираем бельё")
    do_laundry()
    print("\n")

    print("Готовим чашку кофе")
    make_coffee()
    print("\n")

    print("Моем посуду")
    wash_dishes()
    print("\n")

    print("Чистим зубы")
    brush_teeth()
    print("\n")
    make_complex_breakfast()


def make_complex_breakfast():
    print("Готовим комплексный завтрак: ")
    print("1. Готовим яйца....")
    make_breakfast() 
    print("2. Готовим кофе....")
    make_coffee()
    print("Завтрак готов!")

if __name__ == "__main__":
    main()