import random
from collections import Counter
from itertools import combinations

RANKS='23456789TJQKA'
SUITS='shdc'
DECK=[r+s for r in RANKS for s in SUITS]

def rank_five(cards):
    values=sorted((RANKS.index(c[0])+2 for c in cards),reverse=True)
    counts=Counter(values)
    groups=sorted(((n,v) for v,n in counts.items()),reverse=True)
    flush=len({c[1] for c in cards})==1
    uniq=set(values)
    straight=next((hi for hi in range(14,4,-1) if set(range(hi-4,hi+1)).issubset(uniq | ({1} if 14 in uniq else set()))),0)
    if flush and straight:return (8,straight)
    if groups[0][0]==4:return (7,groups[0][1],groups[1][1])
    if groups[0][0]==3 and groups[1][0]==2:return (6,groups[0][1],groups[1][1])
    if flush:return (5,*values)
    if straight:return (4,straight)
    if groups[0][0]==3:return (3,groups[0][1],*sorted((v for v in values if v!=groups[0][1]),reverse=True))
    pairs=sorted((v for n,v in groups if n==2),reverse=True)
    if len(pairs)==2:return (2,*pairs,next(v for v in values if v not in pairs))
    if pairs:return (1,pairs[0],*sorted((v for v in values if v!=pairs[0]),reverse=True))
    return (0,*values)

def rank_seven(cards):
    return max(rank_five(c) for c in combinations(cards,5))

def expand_range(spec):
    spec=spec.strip().upper().replace('10','T')
    if spec in ('','RANDOM','ANY'):
        return list(combinations(DECK,2))
    result=set()
    for raw in spec.split(','):
        token=raw.strip()
        if not token:continue
        plus=token.endswith('+')
        if plus:token=token[:-1]
        if len(token) not in (2,3) or token[0] not in RANKS or token[1] not in RANKS:
            raise ValueError('Invalid range token: '+raw)
        a,b=token[:2]
        suffix=token[2:].lower() if len(token)==3 else ''
        if suffix not in ('','s','o'):raise ValueError('Invalid suitedness: '+raw)
        if a==b:
            if suffix:raise ValueError('Pairs cannot be suited/offsuit')
            ranks=RANKS[RANKS.index(a):] if plus else [a]
            for r in ranks:
                for s1,s2 in combinations(SUITS,2):result.add(tuple(sorted((r+s1,r+s2))))
        else:
            if RANKS.index(a)<=RANKS.index(b):raise ValueError('Use high rank first: '+raw)
            second=RANKS[RANKS.index(b):RANKS.index(a)] if plus else [b]
            for low in second:
                for s1 in SUITS:
                    for s2 in SUITS:
                        if suffix=='s' and s1!=s2:continue
                        if suffix=='o' and s1==s2:continue
                        result.add(tuple(sorted((a+s1,low+s2))))
    if not result:raise ValueError('Empty range')
    return sorted(result)

def simulate(hero,board,opponent_ranges,iterations=2000,seed=None):
    rng=random.Random(seed)
    dead=set(hero+board)
    ranges=[]
    for spec in opponent_ranges:
        combos=[c for c in expand_range(spec) if not (set(c)&dead)]
        if not combos:raise ValueError('Opponent range has no possible hands: '+spec)
        ranges.append(combos)
    wins=ties=losses=0
    equity_sum=0.0
    valid=0
    for _ in range(iterations):
        used=set(dead)
        opponents=[]
        # Retry complete assignment to avoid sequential-card conflicts
        for attempt in range(80):
            used=set(dead);opponents=[]
            for choices in ranges:
                # rejection sampling is exact for single opponent, approximate for joint ranges
                available=[c for c in choices if c[0] not in used and c[1] not in used]
                if not available:break
                hand=rng.choice(available)
                opponents.append(hand);used.update(hand)
            if len(opponents)==len(ranges):break
        if len(opponents)!=len(ranges):continue
        remaining=[c for c in DECK if c not in used]
        runout=board+rng.sample(remaining,5-len(board))
        hero_rank=rank_seven(hero+runout)
        other_ranks=[rank_seven(list(h)+runout) for h in opponents]
        best=max([hero_rank]+other_ranks)
        if hero_rank==best:
            count=1+sum(r==best for r in other_ranks)
            equity_sum+=1/count
            if count==1:wins+=1
            else:ties+=1
        else:losses+=1
        valid+=1
    if not valid:raise ValueError('Cannot assign compatible opponent hands')
    return {'equity':equity_sum/valid,'win_probability':wins/valid,'tie_probability':ties/valid,'loss_probability':losses/valid,'samples':valid,'requested_samples':iterations,'method':'Monte Carlo; equal-weight combos within each range; sequential multi-opponent sampling approximation'}

def calculate_ev(equity,pot,call):
    if call==0:return {'pot_odds':0.0,'call_ev':None,'note':'No call is required; checking and betting require a separate model.'}
    odds=call/(pot+call)
    return {'pot_odds':odds,'call_ev':equity*(pot+call)-call,'note':'Simplified showdown EV: assumes no future betting, no rake, and full equity realization. Pot is measured before hero calls and includes the opponent bet.'}
