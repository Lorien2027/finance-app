#!/usr/bin/env python3
"""Create wheel"""
from glob import glob

from doit.tools import create_folder

DOIT_CONFIG = {'default_tasks': ['all']}


def task_gitclean():
    """Clean all generated files not tracked by git."""
    return {
        'actions': ['git clean -e .doit* -xdf'],
    }


def task_html():
    """Make HTML documentation."""
    return {
        'actions': ['sphinx-build -M html docs build']
    }


def task_pot():
    """Create .pot files."""
    return {
        'actions': ['pybabel extract -o Months.pot FinanceApp'],
        'file_dep': list(glob('FinanceApp/*.py')) + list(glob('FinanceApp/*/*.py')),
        'targets': ['Months.pot'],
    }


def task_po():
    """Update translation."""
    return {
        'actions': ['pybabel update -D Months -d ru -i Months.pot'],
        'file_dep': ['Months.pot'],
        'targets': ['LC_MESSAGES/Months.po'],
    }


def task_mo():
    """Compile translation."""
    return {
        'actions': [
            (create_folder, ['FinanceApp/ru/LC_MESSAGES']),
            'pybabel compile -D Months -l ru -i ru/LC_MESSAGES/Months.po -d FinanceApp'],
        'file_dep': ['ru/LC_MESSAGES/Months.po'],
        'targets': ['FinanceApp/ru/LC_MESSAGES/Months.mo'],
    }


def task_wheel():
    """Create binary wheel distribution."""
    return {
        'actions': ['python -m build -w'],
        'task_dep': ['mo'],
    }


def task_style():
    """flake8 style check."""
    return {
        'actions': ['flake8 FinanceApp']
    }


def task_docstyle():
    """pydocstyle docstrings check."""
    return {
        'actions': ['pydocstyle FinanceApp']
    }


def task_all():
    """Perform all build task."""
    return {
        'actions': None,
        'task_dep': ['gitclean', 'style', 'docstyle', 'html', 'wheel']
    }
