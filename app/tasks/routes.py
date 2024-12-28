# app/tasks/routes.py

from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from bson.objectid import ObjectId  # Import ObjectId
from . import tasks_bp
from flask_paginate import Pagination, get_page_parameter
from .forms import TaskForm
from .. import mongo
from datetime import datetime


@tasks_bp.route('/tasks', methods=['GET'])
@login_required
def list_tasks():
    """List all tasks for the current user with pagination."""
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10  # Number of tasks per page
    total = mongo.db.tasks.count_documents({'user_id': current_user.id})
    user_tasks = mongo.db.tasks.find({'user_id': current_user.id}).skip((page - 1) * per_page).limit(per_page)
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')
    return render_template('tasks/list_tasks.html', tasks=user_tasks, pagination=pagination)


@tasks_bp.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        # Insert the new task with a creation timestamp
        mongo.db.tasks.insert_one({
            'user_id': current_user.id,
            'title': form.title.data,
            'description': form.description.data,
            'completed': False,
            'created_at': datetime.utcnow()  # Add creation timestamp
        })
        flash('Task added successfully!', 'success')
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/add_task.html', form=form)


@tasks_bp.route('/tasks/edit/<task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit an existing task."""
    try:
        oid = ObjectId(task_id)
    except:
        flash('Invalid task ID.', 'danger')
        return redirect(url_for('tasks.list_tasks'))

    task = mongo.db.tasks.find_one({'_id': oid, 'user_id': current_user.id})
    if not task:
        flash('Task not found.', 'danger')
        abort(404)

    form = TaskForm(data=task)
    if form.validate_on_submit():
        mongo.db.tasks.update_one(
            {'_id': oid},
            {'$set': {
                'title': form.title.data,
                'description': form.description.data,
                'completed': form.completed.data
            }}
        )
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/edit_task.html', form=form, task_id=task_id)


@tasks_bp.route('/tasks/delete/<task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete a task."""
    try:
        oid = ObjectId(task_id)
    except:
        flash('Invalid task ID.', 'danger')
        return redirect(url_for('tasks.list_tasks'))

    result = mongo.db.tasks.delete_one({'_id': oid, 'user_id': current_user.id})
    if result.deleted_count:
        flash('Task deleted successfully!', 'success')
    else:
        flash('Task not found or unauthorized.', 'danger')
    return redirect(url_for('tasks.list_tasks'))


@tasks_bp.route('/tasks/complete/<task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    """Mark a task as completed."""
    try:
        oid = ObjectId(task_id)
    except:
        flash('Invalid task ID.', 'danger')
        return redirect(url_for('tasks.list_tasks'))

    task = mongo.db.tasks.find_one({'_id': oid, 'user_id': current_user.id})
    if not task:
        flash('Task not found.', 'danger')
        abort(404)

    if task.get('completed', False):
        flash('Task is already completed.', 'info')
    else:
        mongo.db.tasks.update_one(
            {'_id': oid},
            {'$set': {'completed': True}}
        )
        flash('Task marked as completed!', 'success')

    return redirect(url_for('tasks.list_tasks'))