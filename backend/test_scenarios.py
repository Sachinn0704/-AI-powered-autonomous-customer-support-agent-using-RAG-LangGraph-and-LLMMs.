from agent import process_refund

print("\n========== TEST 1: DELIVERED ORDER ==========")
result1 = process_refund("ORD1001")
print("Decision:", result1["decision"])
print("Reason:", result1["reason"])


print("\n========== TEST 2: SHIPPED ORDER ==========")
result2 = process_refund("ORD1003")
print("Decision:", result2["decision"])
print("Reason:", result2["reason"])


print("\n========== TEST 3: INVALID ORDER ==========")
result3 = process_refund("ORD9999")
print("Decision:", result3["decision"])
print("Reason:", result3["reason"])