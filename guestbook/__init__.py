# coding: utf-8
import pickle
from datetime import datetime
from collections import namedtuple, deque

import click
import netifaces
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
    return render_template('index.html', posts=load_posts())


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


@click.command()
@click.option('--interface', '-i', default='localhost', help='run server on this interface')
@click.option('--port', '-p', default=8000, type=click.IntRange(1, 65535), help='run server on this TCP port')
@click.option('--debug', '-d', default=False, is_flag=True, help='run server in debug mode')
def main(interface, port, debug):
    if interface not in netifaces.interfaces():
        quit('error: interface "%s" not found in %s' % interface, netifaces.interfaces())
    iface = netifaces.interfaces(interface)
    if len(ifaces[netifaces.AF_INET]) + len(ifaces[netifaces.AF_INET6]) == 0:
        quit('error: interface "%s" unbound to an IP address' % interface)
    if len(iface[netifaces.AF_INET]) > 0:
        ipaddr = iface[netifaces.AF_INET][0]['addr']
    else:
        ipaddr = iface[netifaces.AF_INET6][0]['addr']
    application.run(ipaddr, port, debug)