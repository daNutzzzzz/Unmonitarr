from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import db, ArrInstance, UnmonitorRule
from . import scheduler

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    arr_instances = ArrInstance.query.all()
    rules = UnmonitorRule.query.all()
    return render_template('index.html', arr_instances=arr_instances, rules=rules)

@bp.route('/add_instance', methods=['POST'])
def add_instance():
    name = request.form.get('name')
    arr_type = request.form.get('arr_type')
    url = request.form.get('url')
    api_key = request.form.get('api_key')
    sync_interval = int(request.form.get('sync_interval', 3600))
    
    instance = ArrInstance(
        name=name,
        arr_type=arr_type,
        url=url,
        api_key=api_key,
        sync_interval=sync_interval
    )
    db.session.add(instance)
    db.session.commit()
    
    # Reschedule tasks
    scheduler.remove_job(f'sync_{instance.id}')
    scheduler.add_job(
        'tasks.sync_instance',
        trigger='interval',
        seconds=instance.sync_interval,
        args=[instance],
        id=f'sync_{instance.id}'
    )
    
    flash('ARR instance added successfully', 'success')
    return redirect(url_for('main.index'))

@bp.route('/add_rule', methods=['POST'])
def add_rule():
    arr_instance_id = request.form.get('arr_instance')
    quality_profile = request.form.get('quality_profile')
    release_groups = request.form.get('release_groups')
    
    rule = UnmonitorRule(
        arr_instance_id=arr_instance_id,
        quality_profile=quality_profile,
        release_groups=release_groups
    )
    db.session.add(rule)
    db.session.commit()
    
    flash('Rule added successfully', 'success')
    return redirect(url_for('main.index'))

@bp.route('/delete_rule/<int:rule_id>', methods=['POST'])
def delete_rule(rule_id):
    rule = UnmonitorRule.query.get_or_404(rule_id)
    db.session.delete(rule)
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/get_profiles/<int:instance_id>')
def get_profiles(instance_id):
    instance = ArrInstance.query.get_or_404(instance_id)
    # This would make an API call to the ARR instance to fetch quality profiles
    # For now returning a mock response
    return jsonify(['1080p Bluray', '2160p Web-DL', '720p HDTV'])