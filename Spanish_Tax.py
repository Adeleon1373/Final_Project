# Helper function to validate yes/no input
def get_yes_no_input(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ["yes", "no"]:
            return response
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


# Step 1: Ask if the user is a taxable person
def is_taxable_person():
    print("Are you a taxable person according to Spanish tax law?")
    print("You are a taxable person if any of the following apply:")
    print("1. You live in Spain for more than 183 days in a calendar year.")
    print("2. Your main economic activity or business is in Spain.")
    print("3. Your spouse and dependent minor children usually reside in Spain.")

    response = get_yes_no_input("Do any of these apply to you? (yes/no): ")
    return response == "yes"


# Step 2: Ask about exempt income
def get_exempt_income():
    exempt_income = 0.0

    print("\nDo you have any income that is exempt from taxation?")
    print("1. Literary, scientific, or artistic prizes?")
    if get_yes_no_input("   Do you have any such prizes? (yes/no): ") == "yes":
        exempt_income += float(input("   Enter the amount (in euros): €"))

    print("2. Social benefits (e.g., permanent or temporary disability)?")
    if get_yes_no_input("   Do you receive any social benefits? (yes/no): ") == "yes":
        exempt_income += float(input("   Enter the amount (in euros): €"))

    print("3. Public grants or private scholarships?")
    if get_yes_no_input("   Do you receive any grants or scholarships? (yes/no): ") == "yes":
        exempt_income += float(input("   Enter the amount (in euros): €"))

    print("4. Severance pay (up to €180,000 for termination of employment)?")
    if get_yes_no_input("   Did you receive severance pay? (yes/no): ") == "yes":
        exempt_income += float(input("   Enter the amount (in euros): €"))

    print("5. Child support payments (received by children through court decisions)?")
    if get_yes_no_input("   Do your children receive support payments? (yes/no): ") == "yes":
        exempt_income += float(input("   Enter the amount (in euros): €"))

    print("6. Economic benefits for birth, adoption, or childcare?")
    if get_yes_no_input("   Do you receive any such benefits? (yes/no): ") == "yes":
        exempt_income += float(input("   Enter the amount (in euros): €"))

    return exempt_income


# Step 3: Ask about family taxation deductions
def get_family_taxation_deduction():
    print("\nDo you qualify for family taxation deductions?")
    print("1. Two-parent family (€3,400 deduction)?")
    print("2. One-parent family (€2,150 deduction)?")
    while True:
        response = input("Enter 1, 2, or 0 if neither applies: ").strip()
        if response in ["0", "1", "2"]:
            if response == "1":
                return 3400
            elif response == "2":
                return 2150
            else:
                return 0
        else:
            print("Invalid input. Please enter 0, 1, or 2.")


# Step 4: Ask about contributions to social provision systems
def get_social_provision_deduction():
    print("\nDo you have contributions to social provision systems (e.g., pension plans)?")
    if get_yes_no_input("   Do you have any such contributions? (yes/no): ") == "yes":
        contributions = float(input("   Enter the total amount (in euros): €"))
        # Deduction limit: €1,500 (or €10,000 if employer contributions are included)
        limit = 1500
        if get_yes_no_input("   Are employer contributions included? (yes/no): ") == "yes":
            limit = 10000
        return min(contributions, limit)
    else:
        return 0


# Step 5: Ask about personal and family allowances
def get_personal_family_allowances():
    allowances = 0.0

    print("\nDo you have any personal or family allowances?")
    print("1. Descendants (children under 25 or disabled)?")
    if get_yes_no_input("   Do you have any descendants? (yes/no): ") == "yes":
        num_descendants = int(input("   How many descendants? "))
        for i in range(num_descendants):
            age = int(input(f"   Enter age of descendant {i + 1}: "))
            disabled = get_yes_no_input(f"   Is descendant {i + 1} disabled? (yes/no): ") == "yes"
            income = float(input(f"   Enter annual income of descendant {i + 1} (in euros): €"))
            if (age < 25 or disabled) and income <= 8000:
                allowances += 2000  # Example allowance amount (adjust as needed)

    print("2. Ascendants (parents over 65 or disabled)?")
    if get_yes_no_input("   Do you have any ascendants? (yes/no): ") == "yes":
        num_ascendants = int(input("   How many ascendants? "))
        for i in range(num_ascendants):
            age = int(input(f"   Enter age of ascendant {i + 1}: "))
            disabled = get_yes_no_input(f"   Is ascendant {i + 1} disabled? (yes/no): ") == "yes"
            income = float(input(f"   Enter annual income of ascendant {i + 1} (in euros): €"))
            if (age > 65 or disabled) and income <= 8000:
                allowances += 1500  # Example allowance amount (adjust as needed)

    return allowances


# Step 6: Ask about tax credits
def get_tax_credits():
    tax_credits = 0.0

    print("\nDo you qualify for any tax credits?")
    print("1. Investment in shares of new companies/businesses?")
    if get_yes_no_input("   Do you have any such investments? (yes/no): ") == "yes":
        investment = float(input("   Enter the amount invested (in euros): €"))
        tax_credits += min(investment * 0.50, 50000)  # 50% deduction, max €50,000

    print("2. Donations to non-profit organizations or foundations?")
    if get_yes_no_input("   Do you have any such donations? (yes/no): ") == "yes":
        donation = float(input("   Enter the amount donated (in euros): €"))
        if donation <= 150:
            tax_credits += donation * 0.80  # 80% deduction for first €150
        else:
            tax_credits += 150 * 0.80 + (donation - 150) * 0.35  # 35% for the rest

    print("3. Maternity tax credit (for children under 3 years old)?")
    if get_yes_no_input("   Do you qualify for this credit? (yes/no): ") == "yes":
        num_children = int(input("   How many children under 3 years old? "))
        tax_credits += num_children * 1200  # €1,200 per child

    print("4. Large family or disability tax credit?")
    if get_yes_no_input("   Do you qualify for this credit? (yes/no): ") == "yes":
        num_large_family = int(input("   How many large family members? "))
        num_disabled = int(input("   How many disabled family members? "))
        tax_credits += (num_large_family + num_disabled) * 1200  # €1,200 per member

    return tax_credits


# Step 7: Define tax brackets and rates
general_tax_brackets = [
    (0, 12450, 0.19),  # 19% tax for income up to €12,450
    (12451, 20200, 0.24),  # 24% tax for income between €12,451 and €20,200
    (20201, 35200, 0.30),  # 30% tax for income between €20,201 and €35,200
    (35201, 60000, 0.37),  # 37% tax for income between €35,201 and €60,000
    (60001, float('inf'), 0.45)  # 45% tax for income above €60,000
]

savings_tax_brackets = [
    (0, 6000, 0.19),  # 19% tax for income up to €6,000
    (6001, 50000, 0.21),  # 21% tax for income between €6,001 and €50,000
    (50001, 200000, 0.23),  # 23% tax for income between €50,001 and €200,000
    (200001, float('inf'), 0.26)  # 26% tax for income above €200,000
]


# Step 8: Calculate tax for a given income and brackets
def calculate_tax(income, brackets):
    total_tax = 0
    tax_breakdown = []

    for bracket in brackets:
        lower, upper, rate = bracket
        if income > lower:
            taxable_amount = min(income, upper) - lower
            tax = taxable_amount * rate
            total_tax += tax
            tax_breakdown.append((f"€{lower} - €{upper}", f"€{tax:.2f}"))

    return total_tax, tax_breakdown


# Step 9: Main program
if is_taxable_person():
    # Step 10: Input general and savings income
    general_income = float(input("\nEnter your general income (e.g., employment, self-employment, rental income): €"))
    savings_income = float(input("Enter your savings income (e.g., dividends, interest, capital gains): €"))

    # Step 11: Calculate exempt income
    exempt_income = get_exempt_income()
    taxable_general_income = general_income - exempt_income
    taxable_savings_income = savings_income  # Savings income is not reduced by exempt income

    # Step 12: Calculate deductions and allowances
    family_deduction = get_family_taxation_deduction()
    social_provision_deduction = get_social_provision_deduction()
    personal_family_allowances = get_personal_family_allowances()

    # Step 13: Subtract deductions and allowances from taxable income
    taxable_general_income -= (family_deduction + social_provision_deduction + personal_family_allowances)
    if taxable_general_income < 0:
        taxable_general_income = 0  # Ensure taxable income is not negative

    # Step 14: Calculate taxes for general and savings bases
    general_tax, general_breakdown = calculate_tax(taxable_general_income, general_tax_brackets)
    savings_tax, savings_breakdown = calculate_tax(taxable_savings_income, savings_tax_brackets)
    total_tax = general_tax + savings_tax

    # Step 15: Apply tax credits
    tax_credits = get_tax_credits()
    total_tax -= tax_credits
    if total_tax < 0:
        total_tax = 0  # Ensure tax liability is not negative

    # Step 16: Display the results
    print("\nGeneral Tax Breakdown:")
    for bracket, tax in general_breakdown:
        print(f"{bracket}: {tax}")

    print("\nSavings Tax Breakdown:")
    for bracket, tax in savings_breakdown:
        print(f"{bracket}: {tax}")

    print(f"\nTotal Taxable General Income: €{taxable_general_income:.2f}")
    print(f"Total Taxable Savings Income: €{taxable_savings_income:.2f}")
    print(f"Total Tax Credits: €{tax_credits:.2f}")
    print(f"Total Tax Owed: €{total_tax:.2f}")
else:
    print("\nYou are not a taxable person under Spanish tax law. The program will now exit.")