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

debug_enabled = False

def debug(msg = "", end = '\n'):
    if debug_enabled:
        print(msg, end=end)

# N is number of value total, M is number we want to pick (evenly spaced in N)
def select_values(result_array, N, M, start_index = 0, closed_start = True, closed_end = True, allow_optimisation = True, is_inner = False):

    debug(F"___ select_values called with {N}, {M}")
    assert allow_optimisation == False
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

    if N ==0 or M == 0:
        return

    original_n = N


    # values = [0] if closed_start else []



    # the inner call to this func has false for both these vars so we won't end up in here on inner call
    if closed_start or closed_end:
        use_start_index = 1 if closed_start else 0

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
            result_array.append(original_n - 1)

        return


    # we know that closed_start and closed_end are False after here!

    debug(f"====================== is_inner = {is_inner}")
    debug(f"N: {N} M: {M}")

    # avoid division by zero in degenerate case M = 1
    # if M == 1:
    #     debug(f"Got M = 1, so appending N // 2 = [{N // 2}]")
    #     result_array.append(start_index + N // 2)
    #     return

    # with open start and end, we want to use M + 1?!
    # so add one to M - 1 for each of start, end that is open.
    D = N // M
    debug(f"D: {D} (from N, M = {N} {M})")
    
    # Calculate the remainder to adjust spacing
    R = N % M
    debug(f"R: {R}")

    S = (1 + M // R) if R > 0 else None
    debug(f"S: {S}")

    # optimisation: start with entire range if there are more values than holes
    if allow_optimisation and D < 2 and R > 0:
        debug(f">>>>>>>>> optimising, because D = {D} (< 2) and R = {R} (> 0)")

        # I was trying this! no worky.
        # new_n = N if closed else N - 2
        # gap_indexes = select_values(new_n, new_n - M, closed = False, is_inner = True)
        # for 4, 3 this is called with 2, 1

        # gap_indexes = select_values(N - 2, N - M, closed = False, is_inner = True)
        gap_indexes = select_values(N - 2, N - M, is_inner = True, allow_optimisation = allow_optimisation)
        
        debug(f">>>>>>>>> gap_indexes: {gap_indexes} count = {len(gap_indexes)}")

        complete_range = range(N)
        # is_inner shouldn't be true here, anyway
        # if not closed and not is_inner:
        # if closed:
        #     # remove first and last indexes
        #     debug(f"BEFORE {complete_range}")
        #     complete_range = complete_range[1:-1]
        #     debug(f"AFTER {complete_range}")

        numbers = [i for i in complete_range if not i in gap_indexes]

        return numbers

    debug(f">>>>>>>>> NO optimising")

    start_indexo = -D//2

    current_value = start_indexo

    # just a symmetry fix, disable for now
    bump_index_offset = 1 + (S // 2 if S else 0)
    # bump_index_offset = 0

    debug(f"                       >>> S = {S} so bump offset = {bump_index_offset}")

    # for idx in range(0, M - start_indexo):
    # for idx in range(start_indexo, M):
    for idx in range(0, M):
        debug(f"incr: {current_value} + {D} => {current_value + D}")
        current_value += D
        
        # if S and idx > 0 and (idx + bump_index_offset) % S == 0:
        if S and (idx + bump_index_offset) % S == 0:
            debug(f"   ... bumping +1")
            current_value += 1

        debug(f" ------------------------> start_index = {start_index}")
        result_array.append(current_value + start_index)
        # result_array.append(current_value)
    
    debug(f"     ... final array: {result_array}")

# def run(N, M, closed_start = True, closed_end = True, allow_optimisation = True):
def run(N, M, closed_start = True, closed_end = True, allow_optimisation = False): # disabling optimisation completely for now! we assert on it being False elsewhere too
    debug("------------------------------------")
    debug("------------------------------------")
    debug("\n")

    result = []
    select_values(result, N, M, closed_start = closed_start, closed_end = closed_end, allow_optimisation = allow_optimisation)

    debug(f"-->> for N: {N}, M: {M}, closed_st: {closed_start}, closed_end = {closed_end}, allow_optimisation = {allow_optimisation}: {result}  ", end='')

    debug()

    result_str = ""
    for i in range(N):
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
    for n in range(0, max_n + 1):
        # choosing 2 and up, since we've got closed at both ends currently
        for m in range(0, n + 1):
            # print(f"N: {n} M: {m}")
            result_str = run(n, m, closed_start = False, closed_end = False)
            print(f"{result_str}")
            debug(result_str.count("*"))
        print()

exhaustive_test_both_closed(max_n = 20)

print()

# ouch!
# 9  4   .*.*.*.*.
# 9  5   .*.*.*.*.

exhaustive_test_both_open(max_n = 20)

# print(run(5, 2, closed_start = False, closed_end = False))
# print(run(5, 3, closed_start = False, closed_end = False))
# print(run(5, 4, closed_start = False, closed_end = False))

# print(run(8, 5, closed_start = False, closed_end = False))

# print(run(9, 4, closed_start = False, closed_end = False))
# print(run(9, 5, closed_start = False, closed_end = False))

# this produces **..* which isn't very pleasing! Would rather get "*.*.*".

# run(5, 3)
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


# if __name__ == "__main__":
#     import doctest
#     debug_enabled = False
#     doctest.testmod()



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

