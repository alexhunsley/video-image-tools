# generate_inbetween_values.py


# Not well formed currently, in that we can get e.g. this which violates the x or x+1
# occurences of consecutive "*" or ".":
#
# 17 12   *.***.***.***.**.
#
# Oh hold on, CAN this be well-formed? 
# YES, just swap first and last chars:
#
#   ..***.***.***.***   (3 stars everywhere, 2 or 1 dots everywhere)
# 
# I think putting back the optimization (subtracting gaps from full range when D < 2)
# would force * and . symettry for low-high numbers though (e.g. 5 1 and 5 4, etc; generally N, x  and N, N-x).
# Ideally the alg would be symmatrical as-in, without doing this.
#
# Wonder if Bresenhams is naturally symmetrical? It minimises errors, so maybe.
#

# TODO do something about M being low (0 or 1) when one or both ends are open!
# Should it be an error? It shouldn't just be swallowed up, you're requesting
# something bad which shouldn't be glossed over. Unless we take closed start, end
# as hints, not prescriptions! but then you have the problem of "do the flags overide
# the value of M, or does M override the flags", and it's ambiguous and annoying.

# 9  6   *.***.**.
# 12  9   *.****.****.

#
# ok, so 1/3 of the space (N) can be 'missed' (1/6 either side) for unforunate vaues of M ~>= 1/3N up to around (or 2/3N,
# but the 'christmas tree' effect starts much sooner (like M>=30 for N = 500).
#
# One way to deal with this might be to say divide M by 2, then make each 'chunk' be some pattern of appropriate length with two hits in it,
# which won't be divisible by 2, but we just have to fill ensure 2 things roughly fill it. We could use same alg to generate that smaller pattern
# too... recursively until death us do part...?
# Or divide by 4. And so on.
# 

import sys

debug_enabled = False

def debug(msg = "", end = '\n'):
    if debug_enabled:
        print(msg, end=end)


# turn a partition into ascii. 
# Example:
#
#  [1, 3, 2] --> "*..*.*"
def render_partition(p):
    """
    Returns ascii rendering of the given partition using '* and '.' chars.
    >>> render_partition([])
    ''
    >>> render_partition([1])
    '*'
    >>> render_partition([2])
    '.*'
    >>> render_partition([3])
    '..*'
    >>> render_partition([1, 1])
    '**'
    >>> render_partition([1, 1, 1])
    '***'
    >>> render_partition([1, 5, 1])
    '*....**'
    >>> render_partition([1, 2, 3])
    '*.*..*'
    >>> render_partition([0]) # numbers <1 are ignored
    ''
    >>> render_partition([0, -9, -1, -0]) # numbers <1 are ignored
    ''
    >>> render_partition([1, 0, -10, 2]) # numbers <1 are ignored
    '*.*'
    """
    ascii_result = ""

    for p_entry in p:
        if p_entry > 0:
            ascii_result += "." * (p_entry - 1) + "*"

    # do centering. We can't do this on partiiton directly as we can't handle dots that don't end in '*'.

    first_selected_index = ascii_result.find('*')

    if first_selected_index > 1:
        rotate_by = first_selected_index // 2

        left = ascii_result[rotate_by:]
        right = ascii_result[0:rotate_by]

        print(f"patt: {ascii_result} rotate by = {rotate_by} left = {left} right = {right}")

        ascii_result = left + right

    return ascii_result


# 
# the raw partition scheme before optimising to scatter remainder 1s (from end)
# between the non-1 entries at front
def naive_partitions_for_n_split_into_m(N, M):
    """
    Returns array of partitions (ints) for splitting N into M.

    >>> naive_partitions_for_n_split_into_m(0, 0)
    []
    >>> naive_partitions_for_n_split_into_m(0, 1)
    []
    >>> naive_partitions_for_n_split_into_m(0, 123456)
    []
    >>> naive_partitions_for_n_split_into_m(1, 1)
    [1]
    >>> naive_partitions_for_n_split_into_m(2, 2)
    [1, 1]
    >>> naive_partitions_for_n_split_into_m(9, 9)
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
    >>> naive_partitions_for_n_split_into_m(2, 1)
    [1, 1]
    >>> naive_partitions_for_n_split_into_m(3, 2)
    [2, 1]
    >>> naive_partitions_for_n_split_into_m(4, 3)
    [3, 1]
    >>> naive_partitions_for_n_split_into_m(5, 3)
    [3, 1, 1]
    >>> naive_partitions_for_n_split_into_m(6, 3)
    [3, 3]
    >>> naive_partitions_for_n_split_into_m(9, 3)
    [3, 3, 3]
    >>> naive_partitions_for_n_split_into_m(10, 6)
    [6, 1, 1, 1, 1]
    >>> naive_partitions_for_n_split_into_m(10, 9)
    [9, 1]
    >>> naive_partitions_for_n_split_into_m(13, 6)
    [6, 6, 1]
    """

    # short-circuit: N or M being zero gives empty partition
    if N == 0 or M == 0:
        return []

    # short-circuit: choose all indexes gives all 1s
    if N == M:
        return [1] * N

    # D = max size of M repeatable patterns in N
    D = (N // M)
    partitions = [M] * D 

    # remainder
    R = N - M * D
    partitions += [1] * R

    return partitions 


def count_ones_at_end(lst):
    """
    >>> count_ones_at_end([])
    0
    >>> count_ones_at_end([1])
    1
    >>> count_ones_at_end([1, 3])
    0
    >>> count_ones_at_end([3, 3, 2, 1, 1, 1])
    3
    >>> count_ones_at_end([3, 3, 2])
    0
    """
    count = 0
    for element in reversed(lst):
        if element == 1:
            count += 1
        else:
            break
    return count


# Another possible optim:
# *.*       ->  *..*
# *.*.*.*.  ->  *.*..*.*
#
# i.e reverse second half when we have R = 0.
# A bit ott, don't bother at the moment.

def optimised_naive_partition_for_n_split_into_m(naive_partition):
    """
    Returns optimised partition of the given naive_partition.
    This means we attempt to make the partition as symmetrical as possible.
    
    >>> optimised_naive_partition_for_n_split_into_m([])
    []
    >>> optimised_naive_partition_for_n_split_into_m([1])
    [1]
    >>> optimised_naive_partition_for_n_split_into_m([1, 1])
    [1, 1]
    >>> optimised_naive_partition_for_n_split_into_m([1, 1, 1, 1, 1])
    [1, 1, 1, 1, 1]
    >>> optimised_naive_partition_for_n_split_into_m([10, 1])
    [11]
    >>> optimised_naive_partition_for_n_split_into_m([3, 1])
    [4]
    >>> optimised_naive_partition_for_n_split_into_m([4, 4, 4])
    [4, 4, 4]
    >>> optimised_naive_partition_for_n_split_into_m([4, 4, 4, 1])
    [5, 4, 4]
    >>> optimised_naive_partition_for_n_split_into_m([4, 4, 4, 1, 1])
    [5, 4, 5]
    >>> optimised_naive_partition_for_n_split_into_m([2, 2, 2, 2, 2, 1, 1, 1])
    [3, 2, 3, 2, 3]
    >>> optimised_naive_partition_for_n_split_into_m([1, 1]) # from N=3, M=2
    [2, 1]
    """

    # this needs fixing.
    # consider N = 6, M = 4: we will get [1, 1, 1, 1,   1, 1] (1 divides in, 4 times, then the 4 remainder).
    # this needs to become something like [2, 1, 2, 1], so we need the information about the remainder to
    # know what amount of 1s to absorb in previous indexes.
    # from this we need to make 
    if not naive_partition:
        return []

    if naive_partition[0] == 1:
        # nothing to do, iff N == M we end up with an array of all ones.
        return naive_partition

    number_ones_at_end = count_ones_at_end(naive_partition)

    if number_ones_at_end == 0:
        return naive_partition

    # remove ones from end
    balanced_partition = naive_partition[:-number_ones_at_end]

    # distribute 1s between the non-ones remaining
    M = len(balanced_partition)

    # skip factor
    #
    #  Optimisation for improving symmetry.
    #  It selects the end values to achieve that.
    # 
    if number_ones_at_end > 1 and (M - 1) % (number_ones_at_end - 1) == 0:
        # symmetry improvement
        S = (M - 1) // (number_ones_at_end - 1)
        # print(f"1: made S = {S}")
    else:
        S = M // number_ones_at_end
        # print(f"1: made S = {S}")


    loop_index = 0
    partition_index = 0

    while loop_index < number_ones_at_end:
        balanced_partition[partition_index] += 1
        partition_index += S

        loop_index += 1

    return balanced_partition


def optimised_naive_pattern_for_n_split_into_m__B(N, M):
    naive_partition = naive_partitions_for_n_split_into_m(N, M)
    return optimised_naive_pattern_for_n_split_into_m(naive_partition)


def optimised_naive_pattern_for_n_split_into_m(naive_partition):
    optimised_partition = optimised_naive_partition_for_n_split_into_m(naive_partition)
    return f"{naive_partition} {render_partition(optimised_partition)}"

# TOMORROW: add the centering thing. Basically do start_point = (N - partition[0]/2).
# Do this to the partition array? But that can't store notion of dots at end with no * following....

# TODO later call the N M -> partition function so we pass in N M below.
# print(optimised_naive_pattern_for_n_split_into_m([]))
# print(optimised_naive_pattern_for_n_split_into_m([1]))
# print(optimised_naive_pattern_for_n_split_into_m([1, 1]))
# print(optimised_naive_pattern_for_n_split_into_m([2]))
# print(optimised_naive_pattern_for_n_split_into_m([3]))
# print(optimised_naive_pattern_for_n_split_into_m([4]))
# print(optimised_naive_pattern_for_n_split_into_m([2, 2]))
# print(optimised_naive_pattern_for_n_split_into_m([2, 2, 2]))
# print(optimised_naive_pattern_for_n_split_into_m([3, 3, 3]))

# print()

# print(optimised_naive_pattern_for_n_split_into_m([3, 3, 3, 3, 3, 1, 1]))
# print(optimised_naive_pattern_for_n_split_into_m([3, 3, 3, 3, 3, 1, 1, 1]))
# print(optimised_naive_pattern_for_n_split_into_m([3, 3, 3, 3, 3, 1, 1, 1, 1]))
# print(optimised_naive_pattern_for_n_split_into_m([3, 3, 3]))

# print("Result: ", optimised_naive_pattern_for_n_split_into_m__B(5, 3))


# p = [1, 2, 3]
# print(render_partition(p))

# print(optimised_naive_pattern_for_n_split_into_m__B(5, 2))
# print(optimised_naive_pattern_for_n_split_into_m__B(5, 3))


# print(optimised_naive_pattern_for_n_split_into_m__B(20, 11))

print(optimised_naive_pattern_for_n_split_into_m__B(3, 2))


# print(optimised_naive_pattern_for_n_split_into_m__B(200, 67))

sys.exit(0)


# N is number of value total, M is number we want to pick (evenly spaced in N)
def select_values(result_array, N, M, start_index = 0, closed_start = True, closed_end = True, allow_optimisation = True, is_inner = False):

    debug(F"___ select_values called with {N}, {M}")
    # assert allow_optimisation == False
    """
    Select M values from N.

    >>> select_values(3, 3)
    [0, 1, 2]
    >>> select_values(5, 3)
    [0, 2, 4]
    >>> select_values(8, 4)
    [0, 2, 4, 7]
    >>> select_values(9, 4)
    [0, 3, 6, 8]
    >>> select_values(11, 2)
    [0, 10]
    >>> select_values(11, 3)
    [0, 5, 10]
    >>> select_values(11, 4)
    [0, 3, 6, 10]
    >>> select_values(11, 5)
    [0, 2, 5, 7, 10]
    >>> select_values(11, 6)
    [0, 2, 4, 6, 8, 10]
    >>> select_values(11, 11)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    # "    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # >>> select_values(11, 10)

#    >>> select_values(11, 7)
    # [1, 2, 4, 5, 7, 8, 9]
    # >>> select_values(11, 8)
    # [1, 2, 3, 5, 6, 7, 8, 9]
    # >>> select_values(11, 9)
    # >>> select_values(11, 10)

    # short-circuit: choose no indexes
    if N == 0 or M == 0:
        return

    target_range = range(start_index, start_index + N)

    # short-circuit: choose all indexes
    if N == M:
        result_array += target_range
        return

    original_n = N

    # the inner call to this func has false for both these vars so we won't end up in here on inner call
    if closed_start or closed_end:
        use_start_index = start_index + 1 if closed_start else start_index

        if closed_start:
            result_array.append(0)             
            N -= 1
            M -= 1

        if closed_end:
            N -= 1
            M -= 1

        debug(f" BEFORE Inner call, result_array = {result_array}, and calling with N, M = {N} {M}")
        select_values(result_array, N, M, start_index = use_start_index, closed_start = False, closed_end = False, allow_optimisation = allow_optimisation)
        debug(f" AFTER Inner call, result_array = {result_array}")

        if closed_end:
            result_array.append(start_index + original_n - 1)

        return

    # we know that closed_start and closed_end are False after here!
    debug(f"====================== is_inner = {is_inner}")
    debug(f"N: {N} M: {M}")

    # avoid division by zero in degenerate case M = 1
    if M == 1:
        debug(f"Got M = 1, so appending N // 2 = [{N // 2}]")
        result_array.append(start_index + N // 2)
        return

    # with open start and end, we want to use M + 1?!
    # so add one to M - 1 for each of start, end that is open.
    D = (N // M)
    debug(f"D: {D} (from N, M = {N} {M})")
    
    # Calculate the remainder to adjust spacing
    R = N % M
    debug(f"R: {R}")

    S = (1 + M // R) if R > 0 else None
    debug(f"S: {S}")

    # optimisation: start with entire range if there are more values than holes
    if allow_optimisation and D < 2 and R > 0:
        debug(f">>>>>>>>> optimising, because D = {D} (< 2) and R = {R} (> 0)")

        gap_indexes = []
        select_values(gap_indexes, N, N - M, start_index = start_index, closed_start = False, closed_end = False, allow_optimisation = allow_optimisation, is_inner = True)
        
        debug(f">>>>>>>>> gap_indexes: {gap_indexes} count = {len(gap_indexes) if gap_indexes else (None)}")

        index_range_with_gaps_removed = [i for i in target_range if not i in gap_indexes]
        debug(f">>>>>>>>> from range {range} and gap_indexes I've derived index_range_with_gaps_removed = {index_range_with_gaps_removed}")
        result_array += index_range_with_gaps_removed
        return

    debug(f">>>>>>>>> NO optimising")

    gap_at_left = D - 1
    gap_at_right = N - D*M   #N % D
    diff = gap_at_left - gap_at_right

    # -2 below breaks symmetry slightly towards left, -1 the right
    start_indexo = start_index - ((diff - 1) // 2) - 2

    debug(f" <>><>><><<> ({N} {M}) start_indexo = {start_indexo}  (left gap={gap_at_left}, right_gap={gap_at_right} diff = {diff}")
    current_value = start_indexo

    for idx in range(M):
        debug(f"incr: {current_value} + {D} => {current_value + D}")
        current_value += D
        
        # if S and idx > 0 and (idx + bump_index_offset) % S == 0:
        # if S and (idx + bump_index_offset) % S == 0:
        #     debug(f"   ... bumping +1")
        #     current_value += 1

        debug(f" ------------------------> start_index = {start_index}")
        result_array.append(current_value)
    
    debug(f"     ... final array: {result_array}")

# def run(N, M, closed_start = True, closed_end = True, allow_optimisation = True):
def run(N, M, start_index = 0, closed_start = True, closed_end = True, allow_optimisation = True): # disabling optimisation completely for now! we assert on it being False elsewhere too
    debug("------------------------------------")
    debug("------------------------------------")
    debug("\n")

    result = []
    select_values(result, N, M, start_index = start_index, closed_start = closed_start, closed_end = closed_end, allow_optimisation = allow_optimisation)

    debug(f"-->> for N: {N}, M: {M}, closed_st: {closed_start}, closed_end = {closed_end}, allow_optimisation = {allow_optimisation}: {result}  ", end='')

    debug()

    result_str = ""
    # TODO factor out this range, used multiple places
    for i in range(start_index, start_index + N):
        debug(f"Checking i = {i}  ... ", end='')
        if i in result:
            debug("Found i in results, adding *")
            result_str += "*"
            # print("*", end='')
        else:
            debug("Found NO i in results, adding .")
            result_str += "."
            # print(".", end='')

    debug()

    debug(f"__x {result_str} x__")

    # return f"{result_str}"
    debug(f"Should match: count = {result_str.count('*')}, M = {M}, str = {result_str}")
    assert result_str.count("*") == M

    n_formatted = f"{N}".rjust(2)
    m_formatted = f"{M}".rjust(2)
    return f"{n_formatted} {m_formatted}   {result_str}"

# Example Usage
# run(3, 3)
# run(5, 3)

# run(9, 4)
# run(8, 4)

# run(9, 4, False)
# run(8, 4, False)

# run(101, 13, False)
# run(11, 3, False)
# run(11, 2)
# run(11, 3)
# run(11, 4)
# run(11, 5)
# run(11, 6)
# # i.e. 10 and 6, so D=1 for first time
# run(11, 7, False)

# run(4, 3)
# run(4, 3, allow_optimisation = False)


# run(4, 3, closed_start = False, closed_end = False)

# run(4, 2, closed_start = False, closed_end = False)

# run(4, 1, closed_start = False, closed_end = False)


# run(6, 3, closed_start = False, closed_end = False)

# run(6, 3, closed_start = True, closed_end = True)


# # these seem to work ok now
# run(11, 4, closed_start = False, closed_end = False)
# run(11, 4, closed_start = True, closed_end = True)
# run(11, 4, closed_start = True, closed_end = False)
# run(11, 4, closed_start = False, closed_end = True)

# run(33, 6, closed_start = False, closed_end = False)
# run(33, 6, closed_start = True, closed_end = True)
# run(33, 6, closed_start = True, closed_end = False)
# run(33, 6, closed_start = False, closed_end = True)

# run(3, 0)
# run(2, 0)
# run(1, 0)
# run(0, 0)

def exhaustive_test_both_closed(max_n = 10):
    for n in range(2, max_n + 1):
        # choosing 2 and up, since we've got closed at both ends currently
        for m in range(2, n + 1):
            # print(f"N: {n} M: {m}")
            result_str = run(n, m)
            print(f"{result_str}")
            debug(result_str.count("*"))
        print()


def exhaustive_test_both_open(max_n = 10):
    for n in range(max_n, max_n + 1):
        # choosing 2 and up, since we've got closed at both ends currently
        for m in range(0, n + 1):
            # print(f"N: {n} M: {m}")
            result_str = run(n, m, closed_start = False, closed_end = False)
            print(f"{result_str}")
            debug(result_str.count("*"))
        print()


def exhaustive_test_both_open_down_to_d_equals_2(max_n = 10):
    for n in range(0, max_n + 1):
        # choosing 2 and up, since we've got closed at both ends currently
        for m in range(0, n // 2 + 1):
            # print(f"N: {n} M: {m}")
            result_str = run(n, m, closed_start = False, closed_end = False)
            print(f"{result_str}")
            debug(result_str.count("*"))
        print()


# print()

# # ouch!
# # 9  4   .*.*.*.*.
# # 9  5   .*.*.*.*.

# exhaustive_test_both_closed(max_n = 20)
# exhaustive_test_both_open(max_n = 200)
# pathological example:
# .................................*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*..................................
print(run(200, 67, closed_start = False, closed_end = False))

# exhaustive_test_both_open_down_to_d_equals_2()

# print(run(10, 5, closed_start = False, closed_end = False))
# print(run(4, 3, closed_start = False, closed_end = False))
# print(run(4, 4, closed_start = False, closed_end = False))

# print(run(5, 2, closed_start = False, closed_end = False))
# print(run(5, 3, closed_start = False, closed_end = False))
# print(run(5, 4, closed_start = False, closed_end = False))

# print(run(8, 5, closed_start = False, closed_end = False))

# print(run(9, 4, closed_start = False, closed_end = False))
# print(run(9, 5, closed_start = False, closed_end = False))

# this produces **..* which isn't very pleasing! Would rather get "*.*.*".

# run(5, 4)
# run(7, 5, start_index = 0, closed_start = False, closed_end = False)

# run(3, 1, closed_start = False, closed_end = False)




# allow_optimisation is forced to False right now!
# run(5, 3, allow_optimisation = False)

# # run(11, 10)
# run(4, 3)

# run(4, 2)
# # gives '.**.' but really should give '*.*.' or '.*.*',
# # cos closed is a requirement when True but not prescriptive when False
# run(4, 2, closed = False)

# run(4, 1)

# # 
# # this gives '*..*' which is fair enough if you asked for it... (with default closed = True param)
# run(4, 0)
# # this gives '....' as expected
# run(4, 0, closed = False)







# run(11, 7)

# run(101, 101)
# run(4, 3)

# run(3, 3)

# run(99, 96)

# print(select_values(10, 4))  # Example with N = 10, M = 4



# output before doing the symmetry improvement (e43256b):
#
# 2  2   **
# 3  2   *.*
# 3  3   ***
# 4  2   *..*
# 4  3   *.**
# 4  4   ****
# 5  2   *...*
# 5  3   *.*.*
# 5  4   ***.*   <-- bad symmetry
# 5  5   *****
# 6  2   *....*
# 6  3   *..*.*
# 6  4   *.*.**
# 6  5   ****.*   <-- bad symmetry
# 6  6   ******
# 7  2   *.....*
# 7  3   *..*..*
# 7  4   *.*.*.*
# 7  5   **.**.*
# 7  6   *****.*   <-- bad symmetry
# 7  7   *******
# 8  2   *......*
# 8  3   *...*..*
# 8  4   *.*.*..*
# 8  5   *.*.*.**
# 8  6   **.**.**
# 8  7   ******.*
# 8  8   ********
# 9  2   *.......*
# 9  3   *...*...*
# 9  4   *..*..*.*
# 9  5   *.*.*.*.*
# 9  6   *.*.*.*.*
# 9  7   ***.***.*   <-- bad symmetry
# 9  8   *******.*   <-- bad symmetry
# 9  9   *********
#

# after symmetry fix ():
#
# 2  2   **
# 3  2   *.*
# 3  3   ***
# 4  2   *..*
# 4  3   *.**
# 4  4   ****
# 5  2   *...*
# 5  3   *.*.*
# 5  4   **.**
# 5  5   *****
# 6  2   *....*
# 6  3   *..*.*
# 6  4   *.*.**
# 6  5   **.***
# 6  6   ******
# 7  2   *.....*
# 7  3   *..*..*
# 7  4   *.*.*.*
# 7  5   *.**.**
# 7  6   ***.***
# 7  7   *******
# 8  2   *......*
# 8  3   *...*..*
# 8  4   *.*..*.*
# 8  5   *.*.*.**
# 8  6   *.**.***
# 8  7   ***.****
# 8  8   ********
# 9  2   *.......*
# 9  3   *...*...*
# 9  4   *..*..*.*
# 9  5   *.*.*.*.*
# 9  6   *.*.*.*.*
# 9  7   **.***.**
# 9  8   ****.****
# 9  9   *********



if __name__ == "__main__":
    import doctest
    debug_enabled = False
    doctest.testmod()


