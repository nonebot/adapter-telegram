from .parse import Parser
from .generator import gen_api, gen_model

with open("./api.html", "r") as f:
    parser = Parser(f.read())
    gen_api(parser.methods)
