from flask import render_template, flash, redirect, session, request, g, url_for, Response
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.model import User, Category, Question, Slide
from sqlalchemy.exc import IntegrityError

import json


@app.route('/ajax/question/<question_id>/slides', methods=['GET'])
def ajax_slides(question_id):
    resp = { 'status': 'success', 
             'slides': [],
             'slide_count': 0 }
    
    question = Question.query.get(question_id)
    if not question:
        abort(404)
    
    resp['question_id'] = question.id
    resp['slide_count'] = len(question.slides)
    
    for slide in question.slides:
        resp['slides'].append(slide.hashdata)

    return Response(json.dumps(resp), mimetype='application/json')

@app.route('/ajax/slide', methods=['GET'])
def ajax_slide():
    resp = { 'status': 'success' }
    
    slide = Slide.query.get(request.args.get('slide_id'))
    
    if not slide:
        abort(404)
    
    resp['slide'] = slide.hashdata

    return Response(json.dumps(resp), mimetype='application/json')
    
    

@app.route('/ajax/slide', methods=['POST'])
def ajax_slide_save():
    resp = {}

    slide = Slide()
    slide.question_id = request.form.get('question_id')

    slide_id = request.form.get('slide_id')
    
    if slide_id:
        slide = Slide.query.get(slide_id)
        if not slide:
            abort(404)
    
    slide.slide_type = request.form.get('slide_type')
    slide.content    = request.form.get('content')
    slide.prompt     = request.form.get('prompt')
    slide.order_id   = 10
    
    resp['slide_id'] = slide.id
    
    try:
        db.session.add(slide)
        db.session.commit()
    
        resp['status'] = 'success'
        resp['msg'] = 'Slide Saved'
    
    except IntegrityError:
        db.session.rollback()
        
        resp['status'] = 'danger'
        resp['msg'] = e.message
    
    
    return Response(json.dumps(resp), mimetype='application/json')
