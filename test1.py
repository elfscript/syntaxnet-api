import logging
import os, subprocess, fcntl
from syntaxnet_wrapper import parser, language_code_to_model_name

# Overrides available languages map
language_code_to_model_name['en'] = 'English'  # Do not use Parsey McParseface

logging.basicConfig(level=logging.INFO)

#============
def start1(myparser):
        pwd="/usr/local/lib/python2.7/dist-packages/syntaxnet_wrapper"
        rundir = os.path.join(pwd, 'models/syntaxnet/bazel-bin/syntaxnet/parser_eval.runfiles/__main__')
        command = ['python', myparser.run_filename, myparser.model_path, myparser.context_path]

        env = os.environ.copy()
        env['PYTHONPATH'] = rundir
        subproc_args = {'stdin': subprocess.PIPE, 'stdout': subprocess.PIPE,
                        'stderr': subprocess.STDOUT, 'cwd': pwd,
                        'env': env, 'close_fds': True}
        myparser.process = subprocess.Popen(command, shell=False, **subproc_args)
        myparser.out = myparser.process.stdout
        myparser.din = myparser.process.stdin
        fcntl.fcntl(myparser.out.fileno(), fcntl.F_SETFL, fcntl.fcntl(myparser.out.fileno(), fcntl.F_GETFD) | os.O_NONBLOCK)
        myparser.make_pidfile()
        print("start1 done")

#=================
def go(language_code):
    text = u"I am a pig"
    try:
        conllu = parser[language_code].query(text, returnRaw=True)
        if conllu is None:
           logging.error('Bad SyntaxNet output')
        return conllu
    except Exception  as e:
           logging.error(repr(e))

if __name__ == '__main__':
   start1(parser['en'])
   #go('en')
