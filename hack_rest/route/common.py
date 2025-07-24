from hack_rest.database import db
from hack_rest.db_models.business_categories import BusinessCategory


def fetch_all_business_categories():
    """fetch names of all business categories"""
    results = db.session.query(BusinessCategory).all()
    return [{"name": r.name, "loanAmount": r.loan_amount} for r in results]
