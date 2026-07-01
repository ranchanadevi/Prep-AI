from flask import Blueprint, render_template, abort
from models import db
from models.company_questions import CompanyQuestion
from routes.auth import login_required

companies_bp = Blueprint('companies', __name__, url_prefix='/companies')

@companies_bp.route('/')
@login_required
def index():
    # Fetch all company profiles from DB
    companies = CompanyQuestion.query.all()
    return render_template('companies/list.html', companies=companies)

@companies_bp.route('/detail/<int:company_id>')
@login_required
def detail(company_id):
    company = CompanyQuestion.query.get_or_404(company_id)
    return render_template('companies/detail.html', company=company)
