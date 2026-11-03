from agent import process_refund

result = process_refund("ORD1001")

print("\n========== RESOLVEAI AGENT RESULT ==========")

print("Order:", result["order"])
print("Policy:", result["policy"])
print("Customer History:", result["history"])
print("Fraud Check:", result["fraud"])
print("Final Decision:", result["decision"])
print("Reason:", result["reason"])