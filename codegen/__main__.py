import httpx

from .parse import Parser
from .generator import gen_api, gen_model

parser = Parser(httpx.get("https://core.telegram.org/bots/api").text)

with open("./api.py", "w") as f:
    f.write(gen_api(parser.methods))

with open("./model.py", "w") as f:
    f.write(gen_model(parser.types))
