import json
import random


class Bank:
    def __init__(self):
        self.transact_log = 'transact.log'
        self.message = {"id": None,
                        "account": None,
                        "action": None,
                        "amount": None}

        self.action_map = {"open": self.open_account,
                           "withdraw": self.withdraw_funds,
                           "deposit": self.deposit_funds,
                           "transfer": self.transfer_funds,
                           "check": self.check_balance}

    def bank_log_update(self, result=None):
        with open(self.transact_log, mode='a') as log_file:
            log_file.write(result)
        print("log updated")

    def transact(self, message=None, log=None):

        message = json.loads(message)
        account = message["account"]
        action = message["action"]
        funds = message["funds"]
        transact_id = message["id"]

        if account and funds:
            self.action_map[action](account=account, funds=funds)

        if account and not funds:
            self.action_map[action](account=account)

        if funds and not account:
            result = self.action_map[action](funds=funds, transact_id=transact_id)
            self.bank_log_update(result=result)

    def open_account(self, funds=None, transact_id=None):
        account_id = random.randrange(10000, 20000)
        new_account = BankAccount(account_id=account_id, funds=funds)
        return "{} --> NEW ACCOUNT CREATED: {} BALANCE: {}\n". format(transact_id,
                                                                    new_account.account_id,
                                                                    new_account.balance)

    def withdraw_funds(self, account=None, funds=None):
        pass

    def deposit_funds(self, account=None, funds=None):
        pass

    def transfer_funds(self, accounts=None, funds=None):
        pass

    def check_balance(self, account=None):
        pass


    pass


class BankAccount:
    def __init__(self, account_id=0, funds=0):
        self.account_id = account_id
        self.balance = funds
        pass

