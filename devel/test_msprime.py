import msprime
import _msprime
from trees import trees

# msprime.simulate(sample_size=None,
#   Ne=1,
#   length=None,
#   recombination_rate=None,
#   recombination_map=None,
#   mutation_rate=None,
#   population_configurations=None,
#   migration_matrix=None,
#   demographic_events=[],
#   samples=None,
#   random_seed=None,
#   num_replicates=None)

ts = msprime.simulate( sample_size=3, recombination_rate=1.0, random_seed=42 )

# >>> [x for x in ts.records()]
#[ CoalescenceRecord(left=0.1912159270586483,  right=0.8521429346530099,  node=3,  children=(0,  2),  time=0.40566159044942235,  population=0),
#  CoalescenceRecord(left=0.0,                 right=0.1912159270586483,  node=4,  children=(1,  2),  time=0.44077247376386364,  population=0),
#  CoalescenceRecord(left=0.1912159270586483,  right=0.8521429346530099,  node=4,  children=(1,  3),  time=0.44077247376386364,  population=0),
#  CoalescenceRecord(left=0.8521429346530099,  right=1.0,                 node=4,  children=(1,  2),  time=0.44077247376386364,  population=0),
#  CoalescenceRecord(left=0.8521429346530099,  right=1.0,                 node=5,  children=(0,  4),  time=0.7114579294844481,   population=0),
#  CoalescenceRecord(left=0.0,                 right=0.1912159270586483,  node=6,  children=(0,  4),  time=2.8161856234286375,   population=0)]

# >>> [ x.draw(path="tree_{}.svg".format(k)) for k,x in enumerate(ts.trees()) ]
# >>> [ x.get_interval() for x in ts.trees() ]
# Marginal trees are:
#
# 2.8          6
# 0.7         / \                                                                     5
#            /   \                                                                   / \
# 0.44      /     4                           4                                     /   4
#          /     / \                         / \                                   /   / \
# 0.4     /     /   \                       /   3                                 /   /   \
#        /     /     \                     /   / \                               /   /     \
# 0.0   0     1       2                   1   0   2                             0   1       2
#
# (0.0, 0.1912159270586483), (0.1912159270586483, 0.8521429346530099), (0.8521429346530099, 1.0)
#
# Note that 2 inherits from 3 on the whole chromosome but 3 is only specified on the middle interval.

###
# Read records into msprime:
###

my_records = [
    msprime.CoalescenceRecord(left=0.1912159270586483,  right=0.8521429346530099,  node=3,  children=(0,  2),  time=0.40566159044942235,  population=0),
    msprime.CoalescenceRecord(left=0.0,                 right=0.1912159270586483,  node=4,  children=(1,  2),  time=0.44077247376386364,  population=0),
    msprime.CoalescenceRecord(left=0.1912159270586483,  right=0.8521429346530099,  node=4,  children=(1,  3),  time=0.44077247376386364,  population=0),
    msprime.CoalescenceRecord(left=0.8521429346530099,  right=1.0,                 node=4,  children=(1,  2),  time=0.44077247376386364,  population=0),
    msprime.CoalescenceRecord(left=0.8521429346530099,  right=1.0,                 node=5,  children=(0,  4),  time=0.7114579294844481,   population=0),
    msprime.CoalescenceRecord(left=0.0,                 right=0.1912159270586483,  node=6,  children=(0,  4),  time=2.8161856234286375,   population=0)]


my_ll_ts = _msprime.TreeSequence()
my_ll_ts.load_records(my_records)
my_ts = msprime.TreeSequence(my_ll_ts)

[ x==y for x,y in zip( ts.records(), my_ts.records() ) ]

[ x==y for x,y in zip( ts.trees(), my_ts.trees() ) ]

###
# Adjust records
###

# Round down the times:
#
# 1.0          6
# 0.7         / \                                                                     5
#            /   \                                                                   / \
# 0.5       /     4                           4                                     /   4
#          /     / \                         / \                                   /   / \
# 0.4     /     /   \                       /   3                                 /   /   \
#        /     /     \                     /   / \                               /   /     \
# 0.0   0     1       2                   1   0   2                             0   1       2
#          (0.0, 0.2),                   (0.2, 0.8),                             (0.8, 1.0)
#
#
# Note that 2 inherits from 3 on the whole chromosome but 3 is only specified on the middle interval.

###
# Read records into msprime:
###

records = [
    msprime.CoalescenceRecord(left=0.2,  right=0.8,  node=3,  children=(0,  2),  time=0.4,  population=0),
    msprime.CoalescenceRecord(left=0.0,  right=0.2,  node=4,  children=(1,  2),  time=0.5,  population=0),
    msprime.CoalescenceRecord(left=0.2,  right=0.8,  node=4,  children=(1,  3),  time=0.5,  population=0),
    msprime.CoalescenceRecord(left=0.8,  right=1.0,  node=4,  children=(1,  2),  time=0.5,  population=0),
    msprime.CoalescenceRecord(left=0.8,  right=1.0,  node=5,  children=(0,  4),  time=0.7,  population=0),
    msprime.CoalescenceRecord(left=0.0,  right=0.2,  node=6,  children=(0,  4),  time=1.0,  population=0)]


ll_ts = _msprime.TreeSequence()
ll_ts.load_records(records)
ts = msprime.TreeSequence(ll_ts)
for t in trees(list(my_ts.records())):
    print(t)
    pass
print("------------- works in python ----------")

try:
    [ x.draw(path="tree_{}.svg".format(k)) for k,x in enumerate(ts.trees()) ]
    print('works in c')
except:
    pass

# Requirements: (from msprime/lib/tree_sequence.c)
#   Input data must be time sorted.
#   Number of children must be at least 2.
#   Children are non-null and in ascending order
#   'left's must come before 'right's

# Try inserting the invisible 3 in the left and right trees
# by adding a ghost offspring:
#
# 1.0          6
# 0.7         / \                                                                     5
#            /   \                                                                   / \
# 0.5       /     4                           4                                     /   4
#          /     / \                         / \                                   /   / \
# 0.4     /     /   3                       /   3                                 /   /   3
#        /     /   / \                     /   / \                               /   /   / \
#       /     /   7   \                   /   /   \                             /   /   7   \
#      /     /         \                 /   /     \                           /   /         \
# 0.0 0     1           2               1   0       2                         0   1           2
#
#          (0.0, 0.2),                   (0.2, 0.8),                             (0.8, 1.0)


# my_records = [
#     msprime.CoalescenceRecord(left=0.0,  right=0.2,  node=3,  children=(2,  7),  time=0.4,  population=0),  # left seg for 7
#     msprime.CoalescenceRecord(left=0.2,  right=0.8,  node=3,  children=(0,  2),  time=0.4,  population=0),
#     msprime.CoalescenceRecord(left=0.8,  right=1.0,  node=3,  children=(2,  7),  time=0.4,  population=0),  # right seg for 7
#     msprime.CoalescenceRecord(left=0.0,  right=0.2,  node=4,  children=(1,  2),  time=0.5,  population=0),
#     msprime.CoalescenceRecord(left=0.2,  right=0.8,  node=4,  children=(1,  3),  time=0.5,  population=0),
#     msprime.CoalescenceRecord(left=0.8,  right=1.0,  node=4,  children=(1,  2),  time=0.5,  population=0),
#     msprime.CoalescenceRecord(left=0.8,  right=1.0,  node=5,  children=(0,  4),  time=0.7,  population=0),
#     msprime.CoalescenceRecord(left=0.0,  right=0.2,  node=6,  children=(0,  4),  time=1.0,  population=0),
#     ]
#
# my_ll_ts = _msprime.TreeSequence()
# my_ll_ts.load_records(my_records)
# my_ts = msprime.TreeSequence(my_ll_ts)
#
# [ x.draw(path="tree_{}.svg".format(k)) for k,x in enumerate(my_ts.trees()) ]
#
# Error at:
#     if (first_tree) {
#         if (out_count != 0 || in_count != self->sample_size - 1) {
#             ret = MSP_ERR_BAD_COALESCENCE_RECORDS_11;
#             goto out;
#         }

# Same, but renumbered:
#
# 1.0             7
# 0.7            / \                                                                     6
#               /   \                                                                   / \
# 0.5          /     5                           5                                     /   5
#             /     / \                         / \                                   /   / \
# 0.4        /     /   4                       /   4                                 /   /   4
#           /     /   / \                     /   / \                               /   /   / \
#          /     /   3   \                   /   /   \                             /   /   3   \
#         /     /         \                 /   /     \                           /   /         \
# 0.0    0     1           2               1   0       2                         0   1           2
#
#          (0.0, 0.2),                   (0.2, 0.8),                             (0.8, 1.0)


my_records = [
    msprime.CoalescenceRecord(left=0.0,  right=0.2,  node=4,  children=(2,  3),  time=0.4,  population=0),  # left seg for 3
    msprime.CoalescenceRecord(left=0.2,  right=0.8,  node=4,  children=(0,  2),  time=0.4,  population=0),
    msprime.CoalescenceRecord(left=0.8,  right=1.0,  node=4,  children=(2,  3),  time=0.4,  population=0),  # right seg for 3
    msprime.CoalescenceRecord(left=0.0,  right=1.0,  node=5,  children=(1,  4),  time=0.5,  population=0),
    msprime.CoalescenceRecord(left=0.8,  right=1.0,  node=6,  children=(0,  5),  time=0.7,  population=0),
    msprime.CoalescenceRecord(left=0.0,  right=0.2,  node=7,  children=(0,  5),  time=1.0,  population=0),
    ]

my_ll_ts = _msprime.TreeSequence()
my_ll_ts.load_records(my_records)
my_ts = msprime.TreeSequence(my_ll_ts)

for t in trees(list(my_ts.records())):
    print(t)
    pass
print("------------- works in python ----------")
try:
    [ x.draw(path="new_tree_{}.svg".format(k)) for k,x in enumerate(my_ts.trees()) ]
except Exception as e:
    print('fails in c with')
    print('  ', e)

# Error at:

#     if (first_tree) {
#     } else {
#         if (in_count != out_count) {
#             ret = MSP_ERR_BAD_COALESCENCE_RECORDS_12;
#             goto out;
#         }



# Adding whole genome info for phantom
#
# 1.0             8
# 0.7            / \                                                                     7
#               /   \                                                                   / \
# 0.5          /     6                           6                                     /   6
#             /     / \                         / \                                   /   / \
# 0.4        /     /   5                       /   5                                 /   /   5
#           /     /   / \                     /   / \                               /   /   / \
# 0.2      /     /   <   \                   /   4   \                             /   /   <   \
#         /     /     \   \                 /   / \   \                           /   /     \   \
# 0.0    0     1       3   2               1   0   3   2                         0   1       3   2
#
#          (0.0, 0.2),                   (0.2, 0.8),                             (0.8, 1.0)


my_records = [
    msprime.CoalescenceRecord(left=0.2,  right=0.8,  node=4,  children=(0,  3),  time=0.2,  population=0),
    msprime.CoalescenceRecord(left=0.0,  right=0.2,  node=5,  children=(2,  4),  time=0.4,  population=0),
    msprime.CoalescenceRecord(left=0.2,  right=0.8,  node=5,  children=(0,  2),  time=0.4,  population=0),
    msprime.CoalescenceRecord(left=0.8,  right=1.0,  node=5,  children=(2,  4),  time=0.4,  population=0),
    msprime.CoalescenceRecord(left=0.0,  right=1.0,  node=6,  children=(1,  5),  time=0.5,  population=0),
    msprime.CoalescenceRecord(left=0.8,  right=1.0,  node=7,  children=(0,  6),  time=0.7,  population=0),
    msprime.CoalescenceRecord(left=0.0,  right=0.2,  node=8,  children=(0,  6),  time=1.0,  population=0),
    ]

my_ll_ts = _msprime.TreeSequence()
my_ll_ts.load_records(my_records)
my_ts = msprime.TreeSequence(my_ll_ts)
for t in trees(list(my_ts.records())):
    print(t)
    pass
print("------------- imports in python ----------")
# but the trees are not correct
# 	in: CoalescenceRecord(left=0.0, right=0.2, node=5, children=(2, 4), time=0.4, population=0)
#  	in: CoalescenceRecord(left=0.0, right=1.0, node=6, children=(1, 5), time=0.5, population=0)
#  	in: CoalescenceRecord(left=0.0, right=0.2, node=8, children=(0, 6), time=1.0, population=0)
#  ([8, 6, 5, -1, 5, 6, 8, -1, -1], [[], [], [], [], [], (2, 4), (1, 5), [], (0, 6)])
#  	out: CoalescenceRecord(left=0.0, right=0.2, node=8, children=(0, 6), time=1.0, population=0)
#  	out: CoalescenceRecord(left=0.0, right=0.2, node=5, children=(2, 4), time=0.4, population=0)
#  	in: CoalescenceRecord(left=0.2, right=0.8, node=4, children=(0, 3), time=0.2, population=0)
#  	in: CoalescenceRecord(left=0.2, right=0.8, node=5, children=(0, 2), time=0.4, population=0)
#  ([5, 6, 5, 4, -1, 6, -1, -1, -1], [[], [], [], [], (0, 3), (0, 2), (1, 5), [], []])
#  	out: CoalescenceRecord(left=0.2, right=0.8, node=5, children=(0, 2), time=0.4, population=0)
#  	out: CoalescenceRecord(left=0.2, right=0.8, node=4, children=(0, 3), time=0.2, population=0)
#  	in: CoalescenceRecord(left=0.8, right=1.0, node=5, children=(2, 4), time=0.4, population=0)
#  	in: CoalescenceRecord(left=0.8, right=1.0, node=7, children=(0, 6), time=0.7, population=0)
#  ([7, 6, 5, -1, 5, 6, 7, -1, -1], [[], [], [], [], [], (2, 4), (1, 5), (0, 6), []])

for k,x in enumerate(my_ts.trees()):
    print(x)

try:
    [ x.draw(path="new_tree_{}.svg".format(k)) for k,x in enumerate(my_ts.trees()) ]
except Exception as e:
    print('drawing trees fails')
    print(e)

#  doesn't relaly work. Thinks 3 is a root! I'm guessing the alg that draws
#  trees take the first -1 as root and then tries to draw? this would probably
#  happen in the example above too --- if it didn't fail to iterate over trees
#  in c
#  {0: 8, 1: 6, 2: 5, 3: -1, 5: 6, 6: 8, 8: -1}
#  {0: 5, 1: 6, 2: 5, 3: 4, 4: -1, 5: 6, 6: -1}
#  {0: 7, 1: 6, 2: 5, 3: -1, 5: 6, 6: 7, 7: -1}

# so makes sense that drawing trees fails with
# tuple index out of range


# [ x==y for x,y in zip( ts.trees(), my_ts.trees() ) ]
