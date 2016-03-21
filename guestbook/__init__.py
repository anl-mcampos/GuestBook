# coding: utf-8
import pickle
from datetime import datetime
from collections import namedtuple, deque

from flask import Flask, request, render_template, redirect, escape, Markup

application = Flask(__name__)

DATA_FILE = 'guestbook.dat'

Post = namedtuple('Post', ['name', 'timestamp', 'comment'])


def save_post(name, timestamp, comment):
    posts = pickle.load(DATA_FILE)
    assert isinstance(posts, deque)
    posts.appendleft(Post(name, timestamp, comment))
    pickle.dump(posts, DATA_FILE)


def load_posts():
    return pickle.load(DATA_FILE)


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
    return dt.strftime('%d/%m/%Y %H:%M:%S')


def main():
    application.run('127.0.0.1', 8000)


if __name__ == "__main__":
    application.run('127.0.0.1', 8000, debug=True)
