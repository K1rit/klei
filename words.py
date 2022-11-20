from data.json_parser import JSONParser
from setup import *

print()

worker = JSONParser().get_list("data/database.dat", False)

print(worker[level].words_en)
print(worker[level].words_ru)

