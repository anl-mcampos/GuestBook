# coding: utf-8
import pickle
from os.path import exists
from datetime import datetime
from collections import namedtuple, deque

import click
import netifaces
from flask import Flask, request, render_template, redirect, escape, Markup

app = Flask(__name__)

DATA_FILE = 'guestbook.dat'

Post = namedtuple('Post', ['name', 'timestamp', 'comment'])


def save_post(name, timestamp, comment):
    posts = load_posts()
    assert isinstance(posts, deque)
    posts.appendleft(Post(name, timestamp, comment))
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(posts, f)


def load_posts():
    try:
        with open(DATA_FILE, 'rb') as f:
            return pickle.load(f)
    except IOError:
        return deque()


@app.route('/')
def index():
    return render_template('index.html', posts=load_posts())


@app.route('/post', methods=['POST'])
def post():
    name = request.form.get('name')
    comment = request.form.get('comment')
    save_post(name, datetime.now(), comment)
    return redirect('/')


@app.template_filter('nl2br')
def nl2br_filter(s):
    return escape(s).replace('\n', Markup('<br />'))


@app.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    return dt.strftime('%d/%m/%Y %H:%M:%S')


@click.command()
@click.option('--interface', '-i', default='lo', help='run server on this interface [lo]')
@click.option('--port', '-p', default=8000, type=click.IntRange(1, 65535), help='run server on this TCP port [8000]')
@click.option('--debug', '-d', default=False, is_flag=True, help='run server in debug mode')
def main(interface, port, debug):
    if interface not in netifaces.interfaces():
        quit('error: interface "%s" not found in %s' % (interface, netifaces.interfaces()))
    iface = netifaces.ifaddresses(interface)
    if len(iface[netifaces.AF_INET]) + len(iface[netifaces.AF_INET6]) == 0:
        quit('error: interface "%s" unbound to an IP address' % interface)
    if len(iface[netifaces.AF_INET]) > 0:
        ipaddr = iface[netifaces.AF_INET][0]['addr']
    else:
        ipaddr = iface[netifaces.AF_INET6][0]['addr']
    app.run(ipaddr, port, debug)
