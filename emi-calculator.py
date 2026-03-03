from decimal import Decimal, getcontext

# Set high precision for financial calculations
getcontext().prec = 28

## Add Input Function
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


## Add EMI Calculation Function

def calculate_emi(principal, annual_rate, months):
    if annual_rate == 0:
        return principal / Decimal(months)

    monthly_rate = annual_rate / Decimal("12") / Decimal("100")

    one_plus_r_power_n = (Decimal("1") + monthly_rate) ** months

    emi = principal * monthly_rate * one_plus_r_power_n / (one_plus_r_power_n - Decimal("1"))

    return emi


## Add Total Calculation Function

def calculate_totals(emi, principal, months):
    total_payment = emi * Decimal(months)
    total_interest = total_payment - principal

    return total_payment, total_interest


##

def generate_schedule(principal, annual_rate, months, emi):
    schedule = []

    monthly_rate = annual_rate / Decimal("12") / Decimal("100")
    remaining_balance = principal.quantize(Decimal("0.01"))

    for month in range(1, months + 1):

        # Calculate monthly interest (rounded like real banking systems)
        interest = (remaining_balance * monthly_rate).quantize(Decimal("0.01"))

        # Normal principal calculation
        principal_component = (emi - interest).quantize(Decimal("0.01"))

        # Final installment adjustment
        if month == months:
            principal_component = remaining_balance
            emi_adjusted = (principal_component + interest).quantize(Decimal("0.01"))
            remaining_balance = Decimal("0.00")
        else:
            emi_adjusted = emi.quantize(Decimal("0.01"))
            remaining_balance = (remaining_balance - principal_component).quantize(Decimal("0.01"))

        schedule.append({
            "month": month,
            "emi": emi_adjusted,
            "interest": interest,
            "principal": principal_component,
            "balance": remaining_balance
        })

    return schedule

## Add Main Function

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

