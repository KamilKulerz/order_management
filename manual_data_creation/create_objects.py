from orders_app.models import Order, Item, Customer, Category, OrderedItem


def create_cat() -> list[Category]:
    cat_list = []
    for i in range(5):
        cat_list.append(Category.objects.create(name=f'test_cat{i}'))
    return cat_list


def create_item(cat_list: list[Category]) -> list[Item]:
    item_list = []
    for i in range(5):
        item_list.append(Item.objects.create(name=f'test_item{i}',
                                             price=1.5,
                                             category=cat_list[i],
                                             unit='szt.'))
    return item_list


def create_customer() -> list[Customer]:
    cust_list = []
    for i in range(5):
        cust_list.append(Customer.objects.create(name=f'test_customer{i}'))
    return cust_list


def create_order(cust_list: list[Customer]) -> list[Order]:
    order_list = []
    for i in range(5):
        order_list.append(Order.objects.create(customer=cust_list[i],
                                               status=Order.ORDER_STATUSES[0][0]))
    return order_list


def create_ordereditem(item_list: list[Item], order_list: list[Order]) -> None:
    for order in order_list:
        for item in item_list:
            OrderedItem.objects.create(item=item,
                                       quantity=99,
                                       order=order,
                                       status=OrderedItem.ITEM_STATUSES[0][0])


def create_all() -> None:
    cat_list = create_cat()
    it_list = create_item(cat_list)
    cust_list = create_customer()
    ord_list = create_order(cust_list)
    create_ordereditem(it_list, ord_list)
