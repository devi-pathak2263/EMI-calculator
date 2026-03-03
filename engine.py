from decimal import Decimal, getcontext

# Set high precision for financial calculations
getcontext().prec = 28

## EMI Calculation Function

def calculate_emi(principal, annual_rate, months):
    if annual_rate == 0:
        return principal / Decimal(months)

    monthly_rate = annual_rate / Decimal("12") / Decimal("100")

    one_plus_r_power_n = (Decimal("1") + monthly_rate) ** months

    emi = principal * monthly_rate * one_plus_r_power_n / (one_plus_r_power_n - Decimal("1"))

    return emi

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

