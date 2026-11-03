from tools import (
    lookup_order,
    check_refund_policy,
    get_customer_history,
    fraud_check
)

order = lookup_order("ORD1001")

print("\n1. ORDER LOOKUP")
print(order)

print("\n2. REFUND POLICY")
print(check_refund_policy(order))

print("\n3. CUSTOMER HISTORY")
print(get_customer_history(order["customer_id"]))

print("\n4. FRAUD CHECK")
print(fraud_check(order["customer_id"], order["amount"]))