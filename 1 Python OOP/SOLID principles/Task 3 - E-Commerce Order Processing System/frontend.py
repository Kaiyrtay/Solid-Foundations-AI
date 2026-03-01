# ====== FRONTEND: E-COMMERCE MANAGEMENT CONSOLE UI ======

from backend import *

# ====== Dependencies ======
discount_strategy = NoDiscount()
shipping_strategy = StandardShipping()
calculator = PriceCalculator(discount_strategy, shipping_strategy)
validator = OrderValidator()
inventory_service = InventoryService()
loyalty_service = LoyaltyService()
invoice_generator = InvoiceGenerator(calculator)
notifier = EmailNotificationService()
exporter = TXTExport()
payment_processor = CreditCardPayment()

order_service = OrderService(
    validator,
    calculator,
    payment_processor,
    inventory_service,
    loyalty_service,
    invoice_generator,
    notifier,
    exporter
)

# ====== Registries ======
products = {}
customers = {}

# ====== Console UI Functions ======


def print_menu():
    print("\n=== E-Commerce Management System ===")
    print("1. Add Product")
    print("2. Add Customer")
    print("3. Create Order")
    print("4. Process Order")
    print("5. Show Customer Info")
    print("6. Show Product Info")
    print("7. Exit")
    print("8. Export Order/Invoice")

# ----- Add Product -----


def add_product():
    print("\n-- Add Product --")
    try:
        name = input("Name: ").strip()
        category = input("Category: ").strip()
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
        product = Product(name, price, category, stock)
        key = f"{name}_{category}"
        if key in products:
            print(f"[ERROR] Product {name} in {category} already exists.")
            return
        products[key] = product
        print(f"[SUCCESS] Product '{name}' added.")
    except Exception as e:
        print(f"[ERROR] {e}")

# ----- Add Customer -----


def add_customer():
    print("\n-- Add Customer --")
    try:
        name = input("Name: ").strip()
        customer_id = input("Customer ID: ").strip()
        customer = Customer(name, customer_id)
        if customer_id in customers:
            print(f"[ERROR] Customer ID {customer_id} already exists.")
            return
        customers[customer_id] = customer
        print(f"[SUCCESS] Customer '{name}' added.")
    except Exception as e:
        print(f"[ERROR] {e}")

# ----- Create Order -----


def create_order():
    print("\n-- Create Order --")
    customer_id = input("Customer ID: ").strip()
    customer = customers.get(customer_id)
    if not customer:
        print(f"[ERROR] Customer ID {customer_id} not found.")
        return

    items = []
    while True:
        product_name = input("Product Name (or 'done'): ").strip()
        if product_name.lower() == "done":
            break
        category = input("Category: ").strip()
        key = f"{product_name}_{category}"
        product = products.get(key)
        if not product:
            print(f"[ERROR] Product not found.")
            continue
        try:
            qty = int(input("Quantity: ").strip())
            items.append(OrderItem(product, qty))
        except Exception as e:
            print(f"[ERROR] {e}")
            continue

    if not items:
        print("[ERROR] No items added to order.")
        return

    order = Order(customer, items)
    print(f"[SUCCESS] Order created for {customer.name}.")
    return order

# ----- Process Order -----


def process_order(order: Order):
    print("\n-- Process Order --")
    if not order:
        print("[ERROR] No order to process.")
        return
    try:
        result = order_service.process_order(order)
        print(result)
    except Exception as e:
        print(f"[ERROR] {e}")

# ----- Show Customer Info -----


def show_customers():
    print("\n-- Customers --")
    if not customers:
        print("[INFO] No customers found.")
        return
    for c in customers.values():
        print(c)

# ----- Show Product Info -----


def show_products():
    print("\n-- Products --")
    if not products:
        print("[INFO] No products found.")
        return
    for p in products.values():
        print(p)

# ----- Export Order / Invoice -----


def export_order(order: Order):
    if not order:
        print("[ERROR] No order available to export.")
        return

    choice = input("Export as TXT or JSON? ").strip().lower()
    try:
        if choice == "txt":
            exporter = TXTExport()
            print(exporter.export_data(
                order, invoice_generator.generate_invoice(order)))
        elif choice == "json":
            exporter = JSONExport()
            print(exporter.export_data(
                order, invoice_generator.generate_invoice(order)))
        else:
            print("[ERROR] Invalid export type. Choose TXT or JSON.")
    except Exception as e:
        print(f"[ERROR] {e}")

# ====== Main Loop ======


def main():
    current_order = None
    print("Welcome to the E-Commerce Management System!")
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                add_product()
            elif choice == "2":
                add_customer()
            elif choice == "3":
                current_order = create_order()
            elif choice == "4":
                process_order(current_order)
                current_order = None  # Reset after processing
            elif choice == "5":
                show_customers()
            elif choice == "6":
                show_products()
            elif choice == "7":
                print("Goodbye!")
                break
            elif choice == "8":
                export_order(current_order)
            else:
                print("[ERROR] Invalid option. Please choose 1-8.")
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
