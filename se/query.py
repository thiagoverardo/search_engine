from __future__ import annotations
import json
from pysinonimos.sinonimos import Search, historic


class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value


class Tokenizer:
    def __init__(self):
        self.origin = ""
        self.position = 0
        self.tokens = []
        self.actual = None

    def tokenize(self, src):
        self.origin = src
        results = []
        for word in self.origin.split():
            if word.lower() == "and":
                results.append(Token("AND", word))
            elif word.lower() == "or":
                results.append(Token("OR", word))
            else:
                results.append(Token("TERM", word))
        # for result in results:
        #     print(result.type, result.value)
        results.append(Token("EOF", ""))
        self.tokens = results
        return self.tokens

    def nextToken(self):
        if self.position + 1 <= len(self.tokens):
            self.actual = self.tokens[self.position]
            self.position += 1


class Node:
    def evaluate(self, index):
        return set()


class Term(Node):
    def __init__(self, term):
        super().__init__()
        self.term = term

    def evaluate(self, index):
        try:
            return set(index[self.term])
        except:
            return set()


class Operation(Node):
    def __init__(self, nodes: list[Node]):
        super().__init__()
        self.nodes = nodes

    def combine(self, result, new_results):
        return set()

    def evaluate(self, index):
        result = self.nodes[0].evaluate(index)
        for node in self.nodes[1:]:
            result = self.combine(result, node.evaluate(index))
        return result


class OpAnd(Operation):
    def __init__(self, nodes):
        super().__init__(nodes)

    def combine(self, result, new_results):
        return result & new_results


class OpOr(Operation):
    def __init__(self, nodes):
        super().__init__(nodes)

    def combine(self, result, new_results):
        return result | new_results


def build_query(query):
    node_type = query[0]
    if node_type == "term":
        # ["term", "abelha"]
        return Term(query[1])
    else:
        # ["and", ["term", "abelha"], ["term", "rainha"]]
        arg_list = []
        for arg in query[1:]:
            arg_node = build_query(arg)
            arg_list.append(arg_node)
        if node_type == "and":
            return OpAnd(arg_list)
        elif node_type == "or":
            return OpOr(arg_list)
        else:
            raise KeyError(f"Operação {node_type} desconhecida.")


def synonymTrees(terms):
    trees = []
    for term in terms:
        if term not in ["or", "and"]:
            termos = []
            synArg = Search(term)
            synArg = synArg.synonyms()
            if synArg != 404:
                synArg.append(term)
                for syn in synArg:
                    termos.append(Term(syn))
                tree = OpOr(termos)
            else:
                tree = Term(term)
            trees.append(tree)
    return trees


def parseTerm(tk, idx, sTree):
    tk.nextToken()
    if tk.actual.type == "TERM":
        return idx + 1, sTree[idx]


def parseAnd(tk, idx, sTree):
    idx, firstChild = parseTerm(tk, idx, sTree)
    output = firstChild
    if tk.actual.type == "EOF":
        return output
    tk.nextToken()
    while tk.actual.type == "AND":
        idx, secondChild = parseTerm(tk, idx, sTree)
        output = OpAnd([output, secondChild])
        tk.nextToken()
    return idx, output


def parseOr(tk, idx, sTree):
    idx, firstChild = parseAnd(tk, idx, sTree)
    output = firstChild
    while tk.actual.type == "OR":
        idx, secondChild = parseAnd(tk, idx, sTree)
        output = OpOr([output, secondChild])
    return output


def parse_raw_query(raw_query: str):
    query = raw_query.split()
    sTree = synonymTrees(query)
    if len(query) == 1:
        return sTree[0]
    elif len(query) > 1 and len(query) % 2 != 0:
        if query[1].lower() == "or" or query[1].lower() == "and":
            tk = Tokenizer()
            tk.tokenize(raw_query)
            resultado = parseOr(tk, 0, sTree)
            tk.nextToken()
            if tk.actual.type == "EOF":
                return resultado
            else:
                raise Exception("Erro no parser")
        else:
            raise Exception("As queries devem ser ligadas por 'and' ou 'or'")

    raise Exception("Problema na query")


def parse_json_query(json_query: str):
    q = json.loads(json_query)
    print(q)
    query = build_query(q)
    return query
