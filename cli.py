from decimal import Decimal
from engine import calculate_emi, generate_schedule

## Input Function
def get_user_input():
    try:
        principal = Decimal(input("Enter loan amount: "))
        annual_rate = Decimal(input("Enter annual interest rate (%): "))
        months = int(input("Enter tenure (in months): "))

        if principal < 0:
            raise ValueError("Loan amount cannot be negative.")

        if months <= 0:
            raise ValueError("Tenure must be greater than zero.")

        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative.")

        return principal, annual_rate, months

    except Exception as e:
        print(f"Input Error: {e}")
        exit(1)


## Main Function
def main():
    principal, annual_rate, months = get_user_input()

    emi = calculate_emi(principal, annual_rate, months)

    # generate schedule
    schedule = generate_schedule(principal, annual_rate, months, emi)

    #calculate totals from schedule
    total_payment = sum(row["emi"] for row in schedule)
    total_interest = sum(row["interest"] for row in schedule)

    #printing first  3 rows and last row
    print("\nAmortization Schedule (Preview)")
    print("-" * 60)
    print("Month | EMI | Interest | Principal | Balance")

    for row in schedule[:3]:
        print(f"{row['month']} | ₹{row['emi']} | ₹{row['interest']} | ₹{row['principal']} | ₹{row['balance']}")

    print("...")

    last_row = schedule[-1]
    print(f"{last_row['month']} | ₹{last_row['emi']} | ₹{last_row['interest']} | ₹{last_row['principal']} | ₹{last_row['balance']}")
    

    formatted_emi = format(emi.quantize(Decimal("0.01")), ",")
    formatted_interest = format(total_interest.quantize(Decimal("0.01")), ",")
    formatted_payment = format(total_payment.quantize(Decimal("0.01")), ",")


    print("\nLoan Summary")
    print("-" * 30)
    print(f"EMI: ₹{formatted_emi}")
    print(f"Total Interest: ₹{formatted_interest}")
    print(f"Total Payment: ₹{formatted_payment}")


## Add Entry Point
if __name__ == "__main__":
    main()