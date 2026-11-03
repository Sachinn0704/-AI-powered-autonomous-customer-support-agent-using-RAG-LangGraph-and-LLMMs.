from database import SessionLocal
from models import Customer, Order


def seed_data():
    db = SessionLocal()

    try:
        if db.query(Customer).first():
            print("Sample data already exists.")
            return

        customers = [
            Customer(name="Rahul Sharma", email="rahul@example.com"),
            Customer(name="Priya Kumar", email="priya@example.com"),
            Customer(name="Arjun Reddy", email="arjun@example.com")
        ]

        db.add_all(customers)
        db.commit()

        orders = [
            Order(
                order_number="ORD1001",
                customer_id=customers[0].id,
                product="Wireless Headphones",
                amount=2500,
                status="delivered"
            ),
            Order(
                order_number="ORD1002",
                customer_id=customers[1].id,
                product="Smart Watch",
                amount=4500,
                status="delivered"
            ),
            Order(
                order_number="ORD1003",
                customer_id=customers[2].id,
                product="Bluetooth Speaker",
                amount=1800,
                status="shipped"
            )
        ]

        db.add_all(orders)
        db.commit()

        print("Sample customers and orders added successfully!")

    except Exception as error:
        db.rollback()
        print("Error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()