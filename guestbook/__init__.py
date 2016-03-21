# coding: utf-8
import shelve
from contextlib import closing
from datetime import datetime
from collections import namedtuple, deque

from flask import Flask, request, render_template, redirect, escape, Markup

application = Flask(__name__)

DATA_FILE = 'guestbook.dat'

Post = namedtuple('Post', ['name', 'timestamp', 'comment'])


def save_post(name, timestamp, comment):
    with closing(shelve.open(DATA_FILE)) as database:
        greeting_list = database.get('greeting_list', deque())
        assert isinstance(greeting_list, deque)
        greeting_list.appendleft(Post(name, timestamp, comment))
        database['greeting_list'] = greeting_list


def load_posts():
    with closing(shelve.open(DATA_FILE)) as database:
        return database.get('greeting_list', [])


@application.route('/')
def index():
    return render_template('index.html', greeting_list=load_posts())


@application.route('/post', methods=['POST'])
def post():
    name = request.form.get('name')
    comment = request.form.get('comment')
    save_post(name, datetime.now(), comment)
    return redirect('/')


@application.template_filter('nl2br')
def nl2br_filter(s):
    return escape(s).replace('\n', Markup('<br />'))


@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    return dt.strftime('%Y%m%d %H:%M:%S')


def main():
    application.run('127.0.0.1', 8000)


if __name__ == "__main__":
    application.run('127.0.0.1', 8000, debug=True)
