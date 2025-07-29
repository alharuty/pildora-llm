import os
from dotenv import load_dotenv
import replicate

load_dotenv()

print("Token cargado:", os.environ.get("REPLICATE_API_TOKEN"))

output = replicate.run(
    "alharuty/pildora-mll:c2a1d5dab506ec37d0fe8b4cc3ce94e405ef4e5aac8659aaab054b82d866cdd8",
    input={}
)

print(output)