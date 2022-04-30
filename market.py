from time import sleep
from typing import Dict, List, Optional

from models.product import Product
from utils.helper import float_to_str_currency

products: List[Product] = []
shopping_cart: List[Dict[Product, int]] = []


def menu() -> None:
    print(" WELCOME TO THE BEST MARKET YOU'VE EVER SEEN ".center(100, '#'))
    print(" POSSIDERIO'S MARKET ".center(100, '='))

    options = {
        '1': {
            'msg': 'Create a product', 'action': create_product
        },
        '2': {
            'msg': 'Show products', 'action': show_products
        },
        '3': {
            'msg': 'Buy a product', 'action': buy_product
        },
        '4': {
            'msg': 'Show my shopping cart', 'action': show_shopping_cart
        },
        '5': {
            'msg': 'Checkout', 'action': checkout
        },
        '6': {
            'msg': 'Exit', 'action': exit
        },
    }

    checkout_done = False
    while not checkout_done:
        print('\nPlease, choose a number:')
        for i in range(1, len(options.keys()) + 1):
            print(str(i) + ' - ' + options[str(i)]['msg'])
        choice: str = input('\n>>>>>> ')

        try:
            checkout_done = options[str(choice)]['action']()
        except KeyError:
            print('\nYou entered an invalid option. Try again.')
        sleep(0.5)


def main() -> None:
    menu()


def create_product() -> None:
    print('CREATING A PRODUCT'.center(100, '='))
    name: str = input('\nEnter the name of the product: ')
    price: float = float(input('Enter the price of the product: '))

    product: Product = Product(name, price)

    products.append(product)

    print(f'\nThe product {product.name} was created successfully.')


def show_products() -> Optional[bool]:
    if len(products) <= 0:
        print(f'There are no registered products. Try again.')
        return False
    print('PRODUCTS LIST'.center(100, '='))
    for product in products:
        print(product)
        print('---------------------------------')
        sleep(0.5)


def buy_product() -> None:
    check_products = show_products()
    if check_products is False:
        return
    code: int = int(input('\nEnter the code of the product you want to buy: '))

    product: Product = get_product_by_code(code)

    if not product:
        print(f'The product with the code {code} was not found.')
        return
    if len(shopping_cart) == 0:
        item = {product: 1}
        shopping_cart.append(item)
        print(f'The product {product.name} has been added to the shopping cart.')
    else:
        exists_shopping_cart: bool = False
        for item in shopping_cart:
            quantity: int = item.get(product)
            if quantity:
                item[product] = quantity + 1
                print(f'The product {product.name} now has {quantity + 1} units in the shopping cart.')
                exists_shopping_cart = True
        if not exists_shopping_cart:
            prod = {product: 1}
            shopping_cart.append(prod)
            print(f'The product {product.name} has been added to the cart.')


def show_shopping_cart() -> None:
    if len(shopping_cart) <= 0:
        print(f'There are no products in your shopping cart.')
    else:
        print('SHOPPING CART'.center(100, '='))
        for item in shopping_cart:
            for data in item.items():
                print(data[0])
                print(f'Quantity: {data[1]}')
                print('-----------------------------')
                sleep(0.5)


def checkout() -> bool:
    if len(shopping_cart) <= 0:
        print(f'There are no products in your shopping cart.')
        return False
    value: float = 0
    print('CHECKOUT'.center(100, '='))
    for item in shopping_cart:
        for data in item.items():
            print(data[0])
            print(f'Quantity: {data[1]}')
            value += data[0].price * data[1]
            print('-----------------------------')
            sleep(0.5)
    print(f'PURCHASE TOTAL: {float_to_str_currency(value)}. Thank you!')
    shopping_cart.clear()
    return True


def get_product_by_code(code: int) -> Product:
    p: Optional[Product] = None

    for product in products:
        if product.code == code:
            p = product
    return p


if __name__ == "__main__":
    main()
