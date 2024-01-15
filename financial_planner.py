import argparse
import numpy as np
import math
import matplotlib.pyplot as plt
import calendar
import datetime

VALUES = {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', nargs='+', default=None, dest='bank_balances', required=True, help="List of bank balances")
    parser.add_argument('-c', nargs='+', default=None, dest='credit_balances', required=False, help="List of credit card balances")
    parser.add_argument('-p', default=None, dest='pay_rate', required=True, help='Hourly Pay Rate')
    parser.add_argument('-w', default=None, dest='weekly_hours', required=True, help="Hours worked per week")
    parser.add_argument('-t', default=None, dest='tax_rate', required=True, help="Tax rate")
    parser.add_argument('-r', default=None, dest='contribution_rate', required=True, help="Percent contribution to retirement")
    parser.add_argument('-m', default=None, dest='num_months', required=True, help="Number of months to project balance for")
    args = parser.parse_args()

    bank_balances = args.bank_balances
    credit_balances = args.credit_balances
    pay_rate = float(args.pay_rate)
    weekly_hours = float(args.weekly_hours)
    contribution_rate = float(args.contribution_rate)/100.0
    tax_rate = float(args.tax_rate)/100.0
    num_months = int(args.num_months)

    current_time = datetime.datetime.now()
    year = current_time.year
    month = current_time.month
    day = current_time.day

    bank_balance = np.sum(np.asarray([float(value) for value in bank_balances]))
    credit_balance = np.sum(np.asarray([float(value) for value in credit_balances]))

    print(f"Bank Balances: {bank_balances}, Sum: {bank_balance}")
    print(f"Credit Balances: {credit_balances}, Sum: {credit_balance}")
    balance = bank_balance-credit_balance
    print(f"Overall Balance: {balance}")

    monthly_payments = {
        'Rent' : 500,
        'Groceries' : 500,
        'Car Payments' : 200,
        'Gas' : 35,
        'Contacts' : 200,
        'Subscriptions' : 15,
        'Student Loan' : 25
    }

    one_time_payments = {
        'Car Maintenance' : 500,
        'College Payment' : 1235.50,
        'Security Deposit' : 1000,
        'Spikeball Season' : 4000
    }

    one_time_incomes = {
        'Security Deposit' : 500,
        '40 Hour Week' : 786.53
    }

    weekly_hours_dict = {
        calendar.MONDAY : 4,
        calendar.TUESDAY : 7,
        calendar.WEDNESDAY : 4,
        calendar.THURSDAY : 7,
        calendar.FRIDAY : 6
    }

    for payment in one_time_payments:
        balance -= one_time_payments[payment]

    for payment in one_time_incomes:
        balance += one_time_incomes[payment]

    monthly_payment = 0
    for payment in monthly_payments:
        monthly_payment += monthly_payments[payment]

    x = np.arange(0, num_months, 1)
    y = [balance]
    for i in range(1, num_months):
        days = [sum(1 for week in calendar.monthcalendar(year, month) if week[day] != 0) for day in weekly_hours_dict.keys()]
        hours = np.sum(np.asarray([weekly_hours_dict[day]*sum(1 for week in calendar.monthcalendar(year, month) if week[day] != 0) for day in weekly_hours_dict.keys()]))
        monthly_income = round(hours*pay_rate*tax_rate*(1-contribution_rate), 2)

        if month == 12:
            year += 1
        month = ((month) % 12) + 1
        y.append(balance + i*monthly_income - i*monthly_payment)
    plt.plot(x, y, '-o')

    plt.xlabel('Month')
    plt.ylabel('Balance($)')
    plt.title('Balance vs. Months')
    plt.show()

if __name__ == "__main__":
    main()
