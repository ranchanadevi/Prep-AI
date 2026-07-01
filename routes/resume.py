import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from models import db
from models.resume_reports import ResumeReport
from utils.pdf_reader import PDFReader
from utils.gemini_helper import GeminiHelper
from routes.auth import login_required

resume_bp = Blueprint('resume', __name__, url_prefix='/resume')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@resume_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_id = session['user_id']

    if request.method == 'POST':
        # Check if file field is present
        if 'resume' not in request.files:
            flash("No file part selected.", "error")
            return redirect(request.url)
            
        file = request.files['resume']
        
        if file.filename == '':
            flash("No file chosen.", "error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Create a unique filename to prevent namespace clashes
            timestamp = int(os.path.getmtime(current_app.config['UPLOAD_FOLDER'])) if os.path.exists(current_app.config['UPLOAD_FOLDER']) else 0
            unique_filename = f"user_{user_id}_{timestamp}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            try:
                # Save file locally
                file.save(filepath)
                
                # Extract text using PyPDF2
                extracted_text = PDFReader.extract_text(filepath)
                
                if not extracted_text:
                    flash("Unable to parse text from the PDF. Make sure it contains digital text, not scanned images.", "error")
                    # Clean up
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    return redirect(request.url)
                
                # Send to Gemini helper for evaluation
                analysis = GeminiHelper.analyze_resume(extracted_text)
                
                # Check for parsing anomalies
                ats_score = analysis.get('ats_score', 60)
                analysis_string = json.dumps(analysis)

                # Save assessment to database
                report = ResumeReport(
                    user_id=user_id,
                    filename=filename,
                    ats_score=ats_score,
                    analysis_json=analysis_string
                )
                
                db.session.add(report)
                db.session.commit()
                flash("Resume parsed and analyzed successfully!", "success")
                
                # Clean up uploaded physical file
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                return redirect(url_for('resume.report_detail', report_id=report.id))

            except Exception as e:
                db.session.rollback()
                print(f"Error analyzing resume: {e}")
                # Clean up file
                if os.path.exists(filepath):
                    os.remove(filepath)
                flash("An unexpected error occurred during document evaluation.", "error")
                return redirect(request.url)
        else:
            flash("Invalid file type. Only PDF documents (.pdf) are allowed.", "error")
            return redirect(request.url)

    # Fetch past reports
    past_reports = ResumeReport.query.filter_by(user_id=user_id).order_by(ResumeReport.created_at.desc()).all()
    
    return render_template('resume/analyzer.html', reports=past_reports)

@resume_bp.route('/report/<int:report_id>')
@login_required
def report_detail(report_id):
    user_id = session['user_id']
    report = ResumeReport.query.get_or_404(report_id)
    
    # Enforce access control ownership check
    if report.user_id != user_id:
        abort(403)
        
    analysis = report.get_analysis_data()
    return render_template('resume/analyzer.html', active_report=report, analysis=analysis, reports=[])
