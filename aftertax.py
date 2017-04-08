'''
Compute monthly income after tax for year 2017 in Greece
'''
#!/usr/bin/env python3
import argparse
import sys

from collections import OrderedDict


PENSION_PERCENT = 0.067
HEALTH_PERCENT = 0.069
EMPLOYER_PERCENT = 0.1333

MINIMUM_TAXABLE_INCOME = 5600

OVER_THREE_YEARS_TAX = 500  # Telos epithdeumatos because fuck you that's why

TAX_SCALE = OrderedDict(sorted({
    MINIMUM_TAXABLE_INCOME:   0,
    8636:                     0.2,
    20000:                    0.22,
    30000:                    0.29,
    40000:                    0.37,
    10000000000:                0.45
}.items()))


SOLIDARITY_TAX_SCALE = OrderedDict(sorted({
    12000:       0,
    20000:       0.022,
    30000:       0.05,
    40000:       0.065,
    65000:       0.075,
    220000:      0.09,
    10000000000: 0.1

}.items()))


def traverse_tax_scale(income, scale):
    you_got_to_pay = 0
    last_level = MINIMUM_TAXABLE_INCOME
    for level, tax in scale.items():
        print("Level: {0} | Tax: {1}".format(level, tax))
        if income > level:
            you_got_to_pay += level * tax
        else:
            you_got_to_pay += (income - last_level) * tax
            break
        last_level = level
    return you_got_to_pay


def pension_tax(yearly_income, pension_percent):
    return yearly_income * pension_percent


def health_tax(yearly_income, health_percent):
    return yearly_income * health_percent


def taxable_income(yearly_income):
    pension = pension_tax(yearly_income, PENSION_PERCENT)
    health = health_tax(yearly_income, HEALTH_PERCENT)
    yearly_income -= pension
    print("After Pension: {0}".format(yearly_income))
    yearly_income -= health
    print("After Health: {0}".format(yearly_income))
    return yearly_income


def after_tax(yearly_income, over_three_years=False):
    yearly_taxable_income = taxable_income(yearly_income)
    print("Taxable income : {0}".format(yearly_taxable_income))
    taxes = traverse_tax_scale(yearly_taxable_income, TAX_SCALE)
    print("Taxes: {0}".format(taxes))
    solidarity_taxes = traverse_tax_scale(
        yearly_taxable_income, SOLIDARITY_TAX_SCALE)
    print("Solidarity Taxes {0}".format(solidarity_taxes))
    yearly_after = yearly_taxable_income - taxes - solidarity_taxes
    if over_three_years:
        yearly_after -= OVER_THREE_YEARS_TAX
    return yearly_after


def main():
    parser = argparse.ArgumentParser(
        prog='aftertax',
        usage='%(prog) -e monthly number_of_salaries -e ...')
    parser.add_argument(
        '-e', '--employer', nargs='+', action='append',
        help="""
        Pass employer info as tuple. Examples:
            -e 1200 12 -> 12 salaries of 1200
            -e 1300 14 -> 14 salaries of 1300
        """)
    parser.add_argument('-o', '--over-three-years', action='store_true')
    parser.set_defaults(over_three_years=False)

    args = parser.parse_args()
    employers = args.employer

    if len(employers) > 2:
        print("Error: More than to employers follows different tax scheme")
        sys.exit(1)

    yearly_before_tax = 0
    employer_i = 0
    for monthly, number_salaries in employers:
        yearly_employer_income = int(monthly) * int(number_salaries)
        print("Yearly before tax for employer {0}: {1}".format(
            employer_i, yearly_employer_income))
        yearly_before_tax += yearly_employer_income
        employer_i += 1

    print("Yearly before tax: {0}".format(yearly_before_tax))
    yearly_after_tax = after_tax(
        yearly_before_tax, over_three_years=args.over_three_years)
    print("Yearly income after tax: {0}".format(yearly_after_tax))
    print("Monthly income after tax: {0}".format(yearly_after_tax / 12))


if __name__ == "__main__":
    main()
