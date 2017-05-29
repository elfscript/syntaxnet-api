import logging

from syntaxnet_wrapper import parser, language_code_to_model_name

# Overrides available languages map
language_code_to_model_name['en'] = 'English'  # Do not use Parsey McParseface

logging.basicConfig(level=logging.INFO)

#============
def start(self):
        pwd="/usr/local/lib/python2.7/dist-packages/syntaxnet_wrapper"
        rundir = join(pwd, 'models/syntaxnet/bazel-bin/syntaxnet/parser_eval.runfiles/__main__')
        command = ['python', self.run_filename, self.model_path, self.context_path]

        env = os.environ.copy()
        env['PYTHONPATH'] = rundir
        subproc_args = {'stdin': subprocess.PIPE, 'stdout': subprocess.PIPE,
                        'stderr': subprocess.STDOUT, 'cwd': pwd,
                        'env': env, 'close_fds': True}
        self.process = subprocess.Popen(command, shell=False, **subproc_args)
        self.out = self.process.stdout
        self.din = self.process.stdin
        fcntl(self.out.fileno(), F_SETFL, fcntl(self.out.fileno(), F_GETFD) | os.O_NONBLOCK)
        self.make_pidfile()

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
   go('en')
