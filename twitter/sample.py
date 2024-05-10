from itertools import combinations
from collections import Counter
data={'hashtags': [
        ['health', 'autism'],
        ['autism', 'inclusion'],
        ['health', 'autism'],
        ['health', 'autism'],
        ['health', 'disability', 'autism'],
        ['health', 'inclusion', 'disability','autism']
        
    ]}
pair_counts = Counter()

for hashtags_list in data['hashtags']:
    pairs = combinations(hashtags_list, 2)
    pair_counts.update(pairs)

print(pair_counts)