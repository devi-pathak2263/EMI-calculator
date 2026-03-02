from decimal import Decimal, getcontext

# Set high precision for financial calculations
getcontext().prec = 28

## Add Input Function
def get_user_input():
    principal = Decimal(input("Enter loan amount: "))
    annual_rate = Decimal(input("Enter annual interest rate (%): "))
    months = int(input("Enter tenure (in months): "))
    
    return principal, annual_rate, months


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

## Add Main Function

def main():
    principal, annual_rate, months = get_user_input()

    emi = calculate_emi(principal, annual_rate, months)

    total_payment, total_interest = calculate_totals(emi, principal, months)

    print("\nLoan Summary")
    print("-" * 30)
    print(f"EMI: {emi.quantize(Decimal('0.01'))}")
    print(f"Total Interest: {total_interest.quantize(Decimal('0.01'))}")
    print(f"Total Payment: {total_payment.quantize(Decimal('0.01'))}")


## Add Entry Point
if __name__ == "__main__":
    main()

