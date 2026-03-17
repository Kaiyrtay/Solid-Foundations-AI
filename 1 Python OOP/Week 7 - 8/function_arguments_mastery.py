def separator(title: str) -> None:
    print(f"\n{'─' * 10} {title} {'─' * 10}")


def test_att(attr):
    print(f"  value : {attr}")
    print(f"  type  : {type(attr).__name__}")


def test_args(*args):
    for index, value in enumerate(args):
        print(f"  [{index}]  {value!r:<20}  type={type(value).__name__}")


def test_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key:<15} = {value!r}  ({type(value).__name__})")


def test_attr_args(attr, *args):
    print(f"  attr  : {attr!r}  ({type(attr).__name__})")
    print(f"  args  :")
    for index, value in enumerate(args):
        print(f"    [{index}]  {value!r:<20}  type={type(value).__name__}")


def test_attr_kwargs(attr, **kwargs):
    print(f"  attr  : {attr!r}  ({type(attr).__name__})")
    print(f"  kwargs:")
    for key, value in kwargs.items():
        print(f"    {key:<15} = {value!r}  ({type(value).__name__})")


def test_args_kwargs(*args, **kwargs):
    print(f"  args  :")
    for index, value in enumerate(args):
        print(f"    [{index}]  {value!r:<20}  type={type(value).__name__}")
    print(f"  kwargs:")
    for key, value in kwargs.items():
        print(f"    {key:<15} = {value!r}  ({type(value).__name__})")


def test_attr_args_kwargs(attr, *args, **kwargs):
    print(f"  attr  : {attr!r}  ({type(attr).__name__})")
    print(f"  args  :")
    for index, value in enumerate(args):
        print(f"    [{index}]  {value!r:<20}  type={type(value).__name__}")
    print(f"  kwargs:")
    for key, value in kwargs.items():
        print(f"    {key:<15} = {value!r}  ({type(value).__name__})")


pizza = {
    "name":     "Margherita",
    "price":    12.99,
    "vegan":    False,
    "toppings": ["basil", "mozzarella", "tomato"],
}

# separator("test_att")
# test_att(3.14)

# separator("test_args")
# test_args(42, "hello", True, None, 3.14, [1, 2, 3])

# separator("test_kwargs")
# test_kwargs(**pizza)

# separator("test_attr_args")
# test_attr_args("discount", 5, 10, 15, 20)

# separator("test_attr_kwargs")
# test_attr_kwargs("order_001", **pizza)

# separator("test_args_kwargs")
# test_args_kwargs("fast", "extra_cheese", 2, **pizza)

# separator("test_attr_args_kwargs")
# test_attr_args_kwargs(1, 2, 3, 4, 5, 6, **pizza)


def api_call(endpoint, *args, **kwargs):
    url = str(endpoint)

    for segment in args:
        url += f"/{segment}"

    if kwargs:
        params = "&".join(f"{key}={value}" for key, value in kwargs.items())
        url += f"?{params}"

    return url


# print(api_call("some", 2, 3, 4, does_it=None, listing=True))
