from cmd import Cmd
import sys

class Node:
    def __init__(self, name):
        self.entry = False #if True, a word can be formed following path from root to this node
        self.nodes = {} #dictionary of nodes that exist at this node, with key = letter
        self.name = name #letter at this node

class Trie:
    def __init__(self):
        self.root = Node("root")

    def add_word(self, word):
        trav = self.root
        for i in range(len(word)):
            if word[i] in trav.nodes:
                trav = trav.nodes[word[i]]
            else:
                trav.nodes[word[i]] = Node(word[i])
                trav = trav.nodes[word[i]]
        trav.entry = True

    def _get_suggestion(self, n, ret, path):
        if not n:
            return
        if n.entry:
            ret.append(path)
        if n.nodes:
            for k in n.nodes:
                self._get_suggestion(n.nodes[k], ret, path + n.nodes[k].name)

    def get_suggestion(self, preword):
        trav = self.root
        ret = []
        path = ""
        for i in range(len(preword)):
            if preword[i] in trav.nodes:
                trav = trav.nodes[preword[i]]
                path = path + trav.name
        self._get_suggestion(trav, ret, path)
        return ret

    def _print_trie(self, n, path):
        if not n:
            return
        else:
            if n.entry:
                print(path + n.name)
            for k in n.nodes:
                tmp = path
                self._print_trie(n.nodes[k], tmp + n.name)

    def print_trie(self):
        for r in self.root.nodes:
            self._print_trie(self.root.nodes[r], "")
        return

def add_dictionaryWords(t, dictionarypath):
    fl = open(dictionarypath)
    lines = fl.readlines()
    for l in lines:
        t.add_word(l.rstrip())


class MyPrompt(Cmd):
    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit

    def do_maketrie(self, args):
        """Makes a trie with /usr/share/dict/words"""
        add_dictionaryWords(t, "/usr/share/dict/words")
        print("Done creating Trie!")

    def do_insert(self,args):
        """Insert a word into a trie"""
        if len(args) != 0:
            for w in args.split():
                t.add_word(w.rstrip())

    def do_seeTrie(self, args):
        """See your Trie. Warning:if you have a large trie, expect a large output!"""
        t.print_trie()

    def do_suggest(self, args):
        """Ask the trie for suggestions by inputing some prefix"""
        if len(args) != 0:
            l = t.get_suggestion(args)
            for suggestion in l:
                print(suggestion)

    def complete_suggest(self, text, line, start_index, end_index):
        if text:
            return t.get_suggestion(text)
        else:
            return []

t = Trie()
if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting Trie Shell...')
