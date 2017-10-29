import json
import random

# simple bank account with id and balance
class BankAccount:
    def __init__(self, account_id=0, funds=0):
        self.account_id = account_id
        self.balance = funds
        pass

"""
bank with 
    accounts
    log for inbound messages from clients
    log for transactions
    a default message type clients can send
    an action map that relates message actions to bank functions
"""
class Bank:
    def __init__(self):
        self.accounts = {}
        self.message_log = 'messages.log'
        self.transact_log = 'transact.log'

        # default message from client
        # extra keys can be added by client for custom actions, see transfer
        self.message = {"id": None,
                        "account": None,
                        "action": None,
                        "amount": None}

        # map action in received message to action to peform
        # this allows multiple action types to execute same bank function
        self.action_map = {"open": self.open_account,
                           "withdraw": self.withdraw_funds,
                           "deposit": self.deposit_funds,
                           "transfer": self.transfer_funds,
                           "check": self.check_balance}

    # keep history of message and transaction data
    def message_log_update(self, new_message=None):
        with open(self.message_log, mode='a') as log_file:
            log_file.write(new_message)
        print("message log updated")

    def transact_log_update(self, result=None):
        with open(self.transact_log, mode='a') as log_file:
            log_file.write(result)
        print("transact log updated")

    # do a bank transaction based in received message
    def transact(self, message=None, log=None):

        message = json.loads(message)

        # example of handling extra keys from client
        if 'account_from' and 'account_to' in message.keys():
            account_from = message["account_from"]
            account_to = message["account_to"]
            message['account'] = None
        else:
            account_from = None
            account_to = None

        # extract data from message
        account = message["account"]
        action = message["action"]
        funds = message["funds"]
        transact_id = message["id"]

        # open, deposit or withdraw
        if account and funds:
            account, result = self.action_map[action](account=account, funds=funds, transact_id=transact_id)
            self.transact_log_update(result=result)

        # check balance
        if account and not funds:
            account, result = self.action_map[action](account=account, transact_id=transact_id)
            self.transact_log_update(result=result)

        # transfer
        if account_from and account_to:
            account_from, account_to, result = \
                self.action_map[action](account_from=account_from, account_to=account_to,
                                        funds=funds, transact_id=transact_id)
            self.transact_log_update(result=result)
            return account_from, account_to, result

        return account, result

    # new account
    def open_account(self, account=None, funds=None, transact_id=None):
        account_id = account
        new_account = BankAccount(account_id=account, funds=funds)
        self.accounts[account_id] = new_account
        return new_account, \
               "{} --> NEW ACCOUNT CREATED: {} BALANCE: {}\n". format(transact_id,
                                                                      new_account.account_id,
                                                                      new_account.balance)
    # withdraw
    def withdraw_funds(self, account=None, funds=None, transact_id=None):
        if not account or account not in self.accounts:
            return account, "{}: INVALID ACCOUNT\n".format(account)
        else:
            self.accounts[account].balance -= funds
            return self.accounts[account],\
                "{} --> WITHDRAW COMPLETE: {} AMOUNT: {} NEW BALANCE: {}\n"\
                .format(transact_id, self.accounts[account].account_id, funds, self.accounts[account].balance)

    # deposit
    def deposit_funds(self, account=None, funds=None, transact_id=None):
        if not account or account not in self.accounts:
            return account, "{}: INVALID ACCOUNT\n".format(account)
        else:
            self.accounts[account].balance += funds
            return self.accounts[account],\
                "{} --> DEPOSIT COMPLETE: {} AMOUNT: {} NEW BALANCE: {}\n"\
                .format(transact_id, self.accounts[account].account_id, funds, self.accounts[account].balance)

    # transfer
    def transfer_funds(self, account_from=None, account_to=None, funds=None, transact_id=None):
        if not account_from or not account_to:
            return account_from, account_to, "{} : {} INVALID ACCOUNTS\n".format(account_from, account_to)
        else:
            self.accounts[account_from].balance -= funds
            self.accounts[account_to].balance += funds
            return self.accounts[account_from], self.accounts[account_to], \
                   "{} --> TRANSFER COMPLETE: {} AMOUNT: {} NEW BALANCE: {}\n" \
                       .format(transact_id, self.accounts[account_from].account_id, funds, self.accounts[account_to].balance)
    # check balance
    def check_balance(self, account=None, transact_id=None):
        if not account or account not in self.accounts:
            return account, "{}: INVALID ACCOUNT\n".format(account)
        else:
            return self.accounts[account].balance,\
                "{} --> CHECK BALANCE COMPLETED: {} BALANCE: {}\n"\
                .format(transact_id, self.accounts[account].account_id, self.accounts[account].balance)



