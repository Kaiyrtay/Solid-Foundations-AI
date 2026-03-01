from decorators import *

from abc import ABC, abstractmethod

DEFAULT_STANDARD_SHIPPING_COST = 5.0
DEFAULT_EXPRESS_MULTIPLIER = 2.0


class Product:

    def __init__(self, name, price, category, stock_quantity):
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity

    @property
    def name(self):
        return self.__name

    @name.setter
    @str_not_empty("Product name")
    def name(self, value):
        self.__name = value

    @property
    def price(self):
        return self.__price

    @price.setter
    @non_negative_float("Product price")
    def price(self, value):
        self.__price = value

    @property
    def category(self):
        return self.__category

    @category.setter
    @str_not_empty("Product category")
    def category(self, value):
        self.__category = value

    @property
    def stock_quantity(self):
        return self.__stock_quantity

    @stock_quantity.setter
    @non_negative_int("Stock quantity")
    def stock_quantity(self, value):
        self.__stock_quantity = value

    def __hash__(self):
        return hash((self.name, self.category))

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.category == other.category

    def __str__(self):
        return f"{self.name} ({self.category}) - Stock: {self.stock_quantity}"

    def __repr__(self):
        return f"Product(name={self.name}, category={self.category}, stock_quantity={self.stock_quantity})"


class Customer:

    def __init__(self, name, customer_id, loyalty_points=0):
        self.name = name
        self.customer_id = customer_id
        self.loyalty_points = loyalty_points

    @property
    def name(self):
        return self.__name

    @name.setter
    @str_not_empty("Customer name")
    def name(self, value):
        self.__name = value

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    @str_not_empty("Customer ID")
    def customer_id(self, value):
        self.__customer_id = value

    @property
    def loyalty_points(self):
        return self.__loyalty_points

    @loyalty_points.setter
    @non_negative_int("Loyalty points")
    def loyalty_points(self, value):
        self.__loyalty_points = value

    def __hash__(self):
        return hash(self.customer_id)

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return NotImplemented
        return self.customer_id == other.customer_id

    def __str__(self):
        return f"{self.name} (ID: {self.customer_id}) - Loyalty Points: {self.loyalty_points}"

    def __repr__(self):
        return f"Customer(name={self.name}, customer_id={self.customer_id}, loyalty_points={self.loyalty_points})"


class OrderItem:

    def __init__(self, product, quantity):
        if not isinstance(product, Product):
            raise TypeError("product must be a Product instance")
        self.__product = product
        self.quantity = quantity

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, value):
        if not isinstance(value, Product):
            raise TypeError("product must be a Product instance")
        self.__product = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    @non_negative_int("Order item quantity")
    def quantity(self, value):
        self.__quantity = value

    def __hash__(self):
        return hash((self.product, self.quantity))

    def __eq__(self, other):
        if not isinstance(other, OrderItem):
            return NotImplemented
        return self.product == other.product and self.quantity == other.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def __repr__(self):
        return f"OrderItem(product={self.product}, quantity={self.quantity})"


class Order:

    def __init__(self, customer, items):
        if not isinstance(customer, Customer):
            raise TypeError("customer must be a Customer instance")
        if not isinstance(items, list):
            raise TypeError("items must be a list of OrderItem instances")
        for item in items:
            if not isinstance(item, OrderItem):
                raise TypeError("All items must be OrderItem instances")
        self.__customer = customer
        self.__items = list(items)

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, value):
        if not isinstance(value, Customer):
            raise TypeError("customer must be a Customer instance")
        self.__customer = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        if not isinstance(value, list):
            raise TypeError("items must be a list of OrderItem instances")
        for item in value:
            if not isinstance(item, OrderItem):
                raise TypeError("All items must be OrderItem instances")
        self.__items = list(value)

    def __hash__(self):
        return hash((self.customer, tuple(self.items)))

    def __eq__(self, other):
        if not isinstance(other, Order):
            return NotImplemented
        return self.customer == other.customer and self.items == other.items

    def __str__(self):
        items_str = ", ".join(str(item) for item in self.items)
        return f"Order for {self.customer.name}: {items_str}"

    def __repr__(self):
        return f"Order(customer={self.customer}, items={self.items})"


class DiscountStrategy(ABC):

    @abstractmethod
    def calculate_discount(self, order) -> float:
        pass


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage):
        self.percentage = percentage

    @property
    def percentage(self):
        return self.__percentage

    @percentage.setter
    @non_negative_float("Discount percentage")
    def percentage(self, value):
        if value > 100:
            raise ValueError("Discount percentage cannot be greater than 100")
        self.__percentage = value

    def calculate_discount(self, order) -> float:
        total = sum(item.product.price * item.quantity for item in order.items)
        return total * (self.percentage / 100)


class FlatDiscount(DiscountStrategy):

    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    @non_negative_float("Discount amount")
    def amount(self, value):
        self.__amount = value

    def calculate_discount(self, order) -> float:
        return self.amount


class LoyaltyDiscount(DiscountStrategy):

    def __init__(self, points_to_discount_ratio):
        self.points_to_discount_ratio = points_to_discount_ratio

    @property
    def points_to_discount_ratio(self):
        return self.__points_to_discount_ratio

    @points_to_discount_ratio.setter
    @non_negative_float("Points to discount ratio")
    def points_to_discount_ratio(self, value):
        self.__points_to_discount_ratio = value

    def calculate_discount(self, order) -> float:
        return order.customer.loyalty_points * self.points_to_discount_ratio


class NoDiscount(DiscountStrategy):

    def calculate_discount(self, order) -> float:
        return 0.0


class ShippingStrategy(ABC):

    @abstractmethod
    def calculate_shipping_cost(self, order) -> float:
        pass


class StandardShipping(ShippingStrategy):

    def calculate_shipping_cost(self, order) -> float:
        return DEFAULT_STANDARD_SHIPPING_COST


class ExpressShipping(ShippingStrategy):

    def calculate_shipping_cost(self, order) -> float:
        return DEFAULT_STANDARD_SHIPPING_COST * DEFAULT_EXPRESS_MULTIPLIER


class FreeShipping(ShippingStrategy):

    def calculate_shipping_cost(self, order) -> float:
        return 0.0


class PaymentProcessor(ABC):

    @abstractmethod
    def process_payment(self,  amount) -> bool:
        pass


class CreditCardPayment(PaymentProcessor):

    def process_payment(self, amount):
        return True


class PayPalPayment(PaymentProcessor):

    def process_payment(self, amount):
        return True


class PriceCalculator:

    def __init__(self, discount_strategy: DiscountStrategy, shipping_strategy: ShippingStrategy):
        self.discount_strategy = discount_strategy
        self.shipping_strategy = shipping_strategy

    def calculate_total(self, order) -> dict:
        subtotal = sum(item.product.price *
                       item.quantity for item in order.items)
        discount = self.discount_strategy.calculate_discount(order)
        shipping_cost = self.shipping_strategy.calculate_shipping_cost(order)
        total = max(subtotal - discount + shipping_cost, 0.0)

        return {
            "subtotal": subtotal,
            "discount": discount,
            "shipping": shipping_cost,
            "total": total
        }


class OrderValidator:

    def validate(self, order) -> bool:
        if not order.items:
            return False
        for item in order.items:
            if item.quantity > item.product.stock_quantity or item.quantity <= 0:
                return False
        return True


class InventoryService:

    def update_stock(self, order):
        for item in order.items:
            item.product.stock_quantity -= item.quantity


class LoyaltyService:

    def update_loyalty_points(self, order):
        points_earned = sum(item.quantity for item in order.items)
        order.customer.loyalty_points += points_earned


class InvoiceGenerator:

    def __init__(self, price_calculator: PriceCalculator):
        self.price_calculator = price_calculator

    def generate_invoice(self, order) -> str:
        totals = self.price_calculator.calculate_total(order)
        items_str = "\n".join(
            f"{item.product.name} x {item.quantity} @ ${item.product.price:.2f}" for item in order.items)
        invoice = (
            f"Invoice for {order.customer.name}:\n"
            f"{items_str}\n"
            f"Subtotal: ${totals['subtotal']:.2f}\n"
            f"Discount: -${totals['discount']:.2f}\n"
            f"Shipping: +${totals['shipping']:.2f}\n"
            f"Total: ${totals['total']:.2f}"
        )
        return invoice


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: str):
        pass


class EmailNotificationService(NotificationService):
    def send_notification(self, message: str):
        return f"Sending email notification: {message}"


class SMSNotificationService(NotificationService):
    def send_notification(self, message: str):
        return f"Sending SMS notification: {message}"


class Export(ABC):
    @abstractmethod
    def export_data(self, order, invoice_text: str) -> str:
        pass


class JSONExport(Export):
    def export_data(self, order, invoice_text: str) -> str:
        return f"Exporting order for {order.customer.name} in JSON format:\n{invoice_text}"


class TXTExport(Export):
    def export_data(self, order, invoice_text: str) -> str:
        return f"Exporting order for {order.customer.name} in TXT format:\n{invoice_text}"


class OrderService:

    def __init__(self, validator: OrderValidator, calculator: PriceCalculator, payment_processor: PaymentProcessor, inventory_service: InventoryService, loyalty_service: LoyaltyService, invoice_generator: InvoiceGenerator, notification_service: NotificationService, export_service: Export):
        self.validator = validator
        self.calculator = calculator
        self.payment_processor = payment_processor
        self.inventory_service = inventory_service
        self.loyalty_service = loyalty_service
        self.invoice_generator = invoice_generator
        self.notification_service = notification_service
        self.export_service = export_service

    def process_order(self, order) -> str:
        if not self.validator.validate(order):
            return "Order validation failed"

        total = self.calculator.calculate_total(order)

        if not self.payment_processor.process_payment(total["total"]):
            return "Payment processing failed"

        self.inventory_service.update_stock(order)
        self.loyalty_service.update_loyalty_points(order)

        invoice_text = self.invoice_generator.generate_invoice(order)
        export_result = self.export_service.export_data(order, invoice_text)

        notification_message = f"Order for {order.customer.name} processed successfully. Total: ${total['total']:.2f}"
        self.notification_service.send_notification(notification_message)

        return f"{notification_message}\n{export_result}"
