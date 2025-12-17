import csv

PAYMENTS_FILE = "payments.csv"
SETTLEMENTS_FILE = "settlements.csv"


def load_csv(file_name):
    """
    Reads a CSV file and returns a dictionary
    with transaction_id as the key
    """
    data = {}
    with open(file_name, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data[row["transaction_id"]] = row
    return data


def reconcile_payments(payments, settlements):
    matched = []
    amount_mismatch = []
    missing_settlements = []
    extra_settlements = []

    # Check payments against settlements
    for txn_id, payment in payments.items():
        if txn_id in settlements:
            settlement = settlements[txn_id]

            if payment["amount"] == settlement["amount"]:
                matched.append(txn_id)
            else:
                amount_mismatch.append(txn_id)
        else:
            if payment["status"] == "SUCCESS":
                missing_settlements.append(txn_id)

    # Check settlements without payments
    for txn_id in settlements:
        if txn_id not in payments:
            extra_settlements.append(txn_id)

    return matched, amount_mismatch, missing_settlements, extra_settlements


print_report(matched, mismatch, missing, extra)
print_summary(payments, settlements, matched, mismatch, missing, extra)

    print("\nPAYMENT RECONCILIATION REPORT")
    print("=" * 40)

    print(f"Matched Transactions ({len(matched)}):")
    print(matched or "None")

    print("\nAmount Mismatches:")
    print(mismatch or "None")

    print("\nMissing Settlements:")
    print(missing or "None")

    print("\nExtra Settlements:")
    print(extra or "None")


def print_summary(payments, settlements, matched, mismatch, missing, extra):
    print("\nSUMMARY")
    print("-" * 40)

    print(f"Total Payments           : {len(payments)}")
    print(f"Total Settlements        : {len(settlements)}")
    print(f"Matched Transactions     : {len(matched)}")
    print(f"Amount Mismatches        : {len(mismatch)}")
    print(f"Missing Settlements      : {len(missing)}")
    print(f"Extra Settlements        : {len(extra)}")


def main():
    payments = load_csv(PAYMENTS_FILE)
    settlements = load_csv(SETTLEMENTS_FILE)

    matched, mismatch, missing, extra = reconcile_payments(
        payments, settlements
    )

    print_report(matched, mismatch, missing, extra)
    print_summary(payments, settlements, matched, mismatch, missing, extra)


if __name__ == "__main__":
    main()


