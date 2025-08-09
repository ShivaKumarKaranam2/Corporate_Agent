import os
import json
PERSIST_DIR = "C:/Users/karan/OneDrive/Documents/Corporate_Agent/ai-engineer-task-ShivaKumarKaranam2/Corporate Agent/utils/vector_store"
print(os.listdir(PERSIST_DIR))


with open(os.path.join(PERSIST_DIR, "index_store.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))
print(data.keys() if isinstance(data, dict) else data)

