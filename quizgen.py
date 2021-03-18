import sympy
import base64
from sympy import *
from random import randint, sample, shuffle
from tempfile import *
import sys, os

sys.path.append(os.path.realpath(".."))
from quiz import Quiz

''' Helper functions '''

def html(expr):
    return f"\({sympy.latex(expr)}\)"

def insertMovie(filename):
    with open(filename, "rb") as file:
        data = base64.b64encode(file.read()).decode('utf-8')
    type=filename.split(".")[-1].lower()
    #return '<img  src="data:image/' + type + ';base64,' + data + '"/>'
    return '<video width="320" height="240" autoplay controls> <source src="data:video/' + type +';base64,' + data + '"' + 'type="video/mp4"> </video>'

def insertImage(filename):
    with open(filename, "rb") as file:
        data = base64.b64encode(file.read()).decode('utf-8')
    type=filename.split(".")[-1].lower()
    return '<img  src="data:image/' + type + ';base64,' + data + '"/>'

def insertPlot(plt):
    plt.savefig(gettempdir()+'/tmp.png', transparent=True, bbox_inches='tight', pad_inches=0.05)
    return insertImage(gettempdir()+'/tmp.png')
