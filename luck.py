from collections import namedtuple
from tqdm.notebook import tqdm
import random

N = 18300
S = 11

SKILL_WEIGHT = 0.95

get_sample = lambda: random.normalvariate(0, 1)
Candidate = namedtuple('Candidate', ['id', 'luck', 'skill', 'score'])
get_score = lambda skill, luck: SKILL_WEIGHT * skill + (1 - SKILL_WEIGHT) * luck

def create_pool(n=N):
    pool = []
    for i in range(n):
        skill, luck = get_sample(), get_sample()
        score = get_score(skill, luck)
        pool.append(Candidate(i, luck, skill, score))
    return pool

def rank(pool):
    score_list = sorted(pool, key=lambda c: c.score)
    skill_list = sorted(pool, key=lambda c: c.skill)
    luck_list = sorted(pool, key=lambda c: c.luck)
    
    return score_list, skill_list, luck_list


R = 1000
runs = []

for i in tqdm(range(R)):
    pool = create_pool(N)
    score, skill, luck = rank(pool)
    score_result = set([c.id for c in score[-S:]])
    skill_result = set([c.id for c in skill[-S:]])
    luck_result = set([c.id for c in luck[-S:]])
    runs.append(len(score_result & skill_result))

print((1.0 * sum(runs)) / R)
