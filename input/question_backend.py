#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 历史课程

from flask import Blueprint

from handler.base import response

api = Blueprint('history', __name__)


@api.route('/question/<qid>', methods=['GET'])
def get_question(qid):
    return response({})


@api.route('/question/<qid>/knowledge', methods=['GET'])
def get_question_knowledge(qid):
    return response({})


@api.route('/question/list', methods=['GET'])
def list_questions():
    return response({})


@api.route('/knowledge/questions', methods=['GET'])
def get_question_by_knowledge():
    return response({})


@api.route('/knowledge/list', methods=['GET'])
def list_knowledge():
    return response({})
