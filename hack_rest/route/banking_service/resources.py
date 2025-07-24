"""Bank Mock service APIs"""

from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from hack_rest.database import db
from hack_rest.db_models.bank_service import BankAccount, BankBranch
from hack_rest.db_models.group import Group, GroupMember
from hack_rest.route.banking_service.models.bank_account_validate import (
    BANK_ACCOUNT_VALIDATE,
    BANK_VALIDATE_RESPONSE,
)
from hack_rest.route.utils.util_functions import admin_required

BANK_SERVICE_NS = Namespace("bank", description="Banking Service APIs")

BANK_SERVICE_NS.models[BANK_ACCOUNT_VALIDATE.name] = BANK_ACCOUNT_VALIDATE
BANK_SERVICE_NS.models[BANK_VALIDATE_RESPONSE.name] = BANK_VALIDATE_RESPONSE


@BANK_SERVICE_NS.route("/<group_id>/loan_distribute")
class LoanDistribute(Resource):
    """Distribute Loan"""

    @admin_required
    def post(self, group_id: int):
        """
        Distribute Loan
        """
        distribution_amount = request.json.get("distribution_amount")
        account_numbers = (
            db.sessions.query(BankAccount.account_number)
            .join(GroupMember, BankAccount.aadhar_number == GroupMember.aadhar_number)
            .filter(GroupMember.group_id == group_id)
            .all()
        )
        if account_numbers:
            amount_each_member = distribution_amount / len(account_numbers)
            for account_number in account_numbers:
                account = (
                    db.session.query(BankAccount)
                    .filter(BankAccount.account_number == account_number)
                    .first()
                )
                account.balance += amount_each_member
                db.session.add(account)
            db.session.commit()

            return {
                "message": "Loan distributed successfully",
            }, HTTPStatus.OK
        else:
            return {
                "message": "No accounts found for this group",
            }, HTTPStatus.BAD_REQUEST


@BANK_SERVICE_NS.route("/validate")
class BankAccountValidate(Resource):
    """Validate Bank Account"""

    @BANK_SERVICE_NS.expect(BANK_ACCOUNT_VALIDATE)
    @BANK_SERVICE_NS.marshal_with(BANK_VALIDATE_RESPONSE)
    @admin_required
    def post(self):
        """
        Validate Bank Account
        """

        data = request.json

        account = (
            db.session.query(BankAccount)
            .join(BankBranch, BankAccount.branch_id == BankBranch.branch_id)
            .filter(
                BankAccount.account_number == data["account_number"],
                BankAccount.aadhar_number == data["aadhar_number"],
                BankAccount.pan_card_number == data["pan_number"],
                BankBranch.ifsc_code == data["ifsc_code"],
                BankAccount.mobile_number == data["mobile_number"],
            )
            .first()
        )

        if not account:
            return {
                "valid": False,
                "message": "Details are not valid",
            }, HTTPStatus.BAD_REQUEST

        return {"valid": True, "message": "Details are valid"}, HTTPStatus.OK


@BANK_SERVICE_NS.route("")
class Bank(Resource):
    """Bank Related APIs"""

    def get(self):
        """
        Get Bank Details
        """
        banks = db.session.query(Bank).all()
        bank_details = []
        for bank in banks:
            bank_details.append({"bank_id": bank.bank_id, "bank_name": bank.bank_name})
        return {"banks": bank_details}, HTTPStatus.OK

    def post(self):
        """
        Add Bank
        """
        data = request.json
        bank = Bank(bank_name=data["bank_name"])
        db.session.add(bank)
        db.session.commit()
        return {"message": "Bank added successfully"}, HTTPStatus.OK


@BANK_SERVICE_NS.route("/branch")
class BankBranch(Resource):
    """Bank Branch Related APIs"""

    def get(self):
        """
        Get Bank Branch Details
        """
        bank_branches = db.session.query(BankBranch).all()
        bank_branch_details = []
        for bank_branch in bank_branches:
            bank_branch_details.append(
                {
                    "branch_id": bank_branch.branch_id,
                    "ifsc_code": bank_branch.ifsc_code,
                    "branch_address": bank_branch.branch_address,
                    "bank_id": bank_branch.bank_id,
                }
            )
        return {"bank_branches": bank_branch_details}, HTTPStatus.OK

    def post(self):
        """
        Add Bank Branch
        """
        data = request.json
        bank_branch = BankBranch(
            ifsc_code=data["ifsc_code"],
            branch_address=data["branch_address"],
            bank_id=data["bank_id"],
        )
        db.session.add(bank_branch)
        db.session.commit()
        return {"message": "Bank branch added successfully"}, HTTPStatus.OK


@BANK_SERVICE_NS.route("/account")
class BankAccount(Resource):
    """Bank Account Related APIs"""

    def get(self):
        """
        Get Bank Account Details
        """
        bank_accounts = db.session.query(BankAccount).all()
        bank_account_details = []
        for bank_account in bank_accounts:
            bank_account_details.append(
                {
                    "account_number": bank_account.account_number,
                    "user_name": bank_account.user_name,
                    "balance": bank_account.balance,
                    "aadhar_number": bank_account.aadhar_number,
                    "pan_card_number": bank_account.pan_card_number,
                    "account_type": bank_account.account_type,
                    "mobile_number": bank_account.mobile_number,
                    "email_id": bank_account.email_id,
                    "branch_id": bank_account.branch_id,
                }
            )
        return {"bank_accounts": bank_account_details}, HTTPStatus.OK

    def post(self):
        """
        Add Bank Account
        """
        data = request.json
        bank_account = BankAccount(
            account_number=data["account_number"],
            user_name=data["user_name"],
            balance=data["balance"],
            aadhar_number=data["aadhar_number"],
            pan_card_number=data["pan_card_number"],
            account_type=data["account_type"],
            mobile_number=data["mobile_number"],
            email_id=data["email_id"],
            branch_id=data["branch_id"],
        )
        db.session.add(bank_account)
        db.session.commit()
        return {"message": "Bank account added successfully"}, HTTPStatus.OK
