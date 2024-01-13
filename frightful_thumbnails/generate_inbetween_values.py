# generate_inbetween_values.py

# TODO do something about M being low (0 or 1) when one or both ends are open!
# Should it be an error? It shouldn't just be swallowed up, you're requesting
# something bad which shouldn't be glossed over. Unless we take closed start, end
# as hints, not prescriptions! but then you have the problem of "do the flags overide
# the value of M, or does M override the flags", and it's ambiguous and annoying.


debug_enabled = True

def debug(msg, end='\n'):
    if debug_enabled:
        print(msg, end=end)

# N is number of value total, M is number we want to pick (evenly spaced in N)
def select_values(result_array, N, M, start_index = 0, closed_start = True, closed_end = True, allow_optimisation = True, is_inner = False):
    print(f" SADASDASDSADSADASDASDSADSADASDASD allow_optimisation = {allow_optimisation}")

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

    if closed_start:
        # if closed_start is true, we're not in a inner call, so we know the start index is 0
        result_array.append(0) 
    # values = [0] if closed_start else []



    # the inner call to this func has false for both these vars so we won't end up in here on inner call
    if closed_start or closed_end:
        use_start_index = 1 if closed_start else 0

        if closed_start:
            N -= 1
            M -= 1

        if closed_end:
            N -= 1
            M -= 1

        print(f" BEFORE Inner call, result_array = {result_array}, and calling with N, M = {N} {M}")
        select_values(result_array, N, M, start_index = use_start_index, closed_start = False, closed_end = False, allow_optimisation = allow_optimisation)
        print(f" AFTER Inner call, result_array = {result_array}")

        if closed_end:
            result_array.append(original_n - 1)

        return

    debug(f"====================== is_inner = {is_inner}")
    debug(f"N: {N} M: {M}")

    # avoid division by zero in degenerate case M = 1
    if M == 1:
        debug(f"Got M = 1, so appending N // 2 = [{N // 2}]")
        result_array.append(start_index + N // 2)
        return

    # if not closed and not is_inner:
    # # if not closed:
    #     # we're not having items at first, last index, so add 2 to M
    #     print(f" ()() adding 2 to M, now got M = {M}")
    #     M += 2

    # use_m = M - 1
    use_m = M + 1

    use_n = N + 1

    # if not closed_start: 
    #     use_m += 1
    # if not closed_end: 
    #     use_m += 1

    # with open start and end, we want to use M + 1?!
    # so add one to M - 1 for each of start, end that is open.
    D = use_n // use_m
    debug(f"D: {D}")
    
    # Calculate the remainder to adjust spacing
    R = use_n % use_m
    debug(f"R: {R}")

    S = use_m // R if R > 0 else None
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

    # Initialize the list of values, starting with 0
    
    # values = [0] if closed else []
    debug(f">>>>>>>>> NO optimising")

    

    spaces = N - M
    debug(f"spaces: {spaces}")

    # Current value
    current_value = 0 if closed_start else -1

    # every time bump % S == 0 we increment current_value by 1
    bump_index = 0
    
    # for idx in range(0, M - 2):
    for idx in range(0, M):
        # Add the interval D to the current value
        current_value += D
        
        # if idx < (M - 2) and S and (idx + 1) % S == 0:
        if S and (idx + 1) % S == 0:
            current_value += 1

        bump_index += 1
    #     # Distribute the remainder evenly across the intervals
    #     if R > 0:
    #         current_value += 1
    #         remainder -= 1
        
    #     # Add the current value to the list
        print(f" ------------------------> start_index = {start_index}")
        result_array.append(current_value + start_index)
        # result_array.append(current_value)
    
    # # Always include N as the last value
    # values.append(N)

    # if closed:  
    #     values.append(N - 1)

    # return values


# def run(N, M, closed_start = True, closed_end = True, allow_optimisation = True):
def run(N, M, closed_start = True, closed_end = True, allow_optimisation = False): # disabling optimisation completely for now! we assert on it being False elsewhere too
    debug("------------------------------------")
    debug("------------------------------------")
    debug("\n")

    result = []
# result_array, N, M, start_index = 0, closed_start = True, closed_end = True, allow_optimisation = True, is_inner = False)
    select_values(result, N, M, closed_start = closed_start, closed_end = closed_end, allow_optimisation = allow_optimisation)

    debug(f"-->> for N: {N}, M: {M}, closed_st: {closed_start}, closed_end = {closed_end}, allow_optimisation = {allow_optimisation}: {result}  ", end='')

    # asci repr

    print()

    result_str = ""
    for i in range(N):
        print(f"Checking i = {i}  ... ", end='')
        if i in result:
            print("Found i in results, adding *")
            result_str += "*"
            # print("*", end='')
        else:
            print("Found NO i in results, adding .")
            result_str += "."
            # print(".", end='')
    print()

    print(f"__x {result_str} x__")

    return result_str

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

def exhastive_test():
    for n in range(2, 4):
        # choosing 2 and up, since we've got closed at both ends currently
        for m in range(2, n + 1):
            # print(f"N: {n} M: {m}")
            result_str = run(n, m)
            print(result_str.count("*"))


# exhastive_test()

# this produces **..* which isn't very pleasing! Would rather get "*.*.*".

run(5, 3)

run(3, 1, closed_start = False, closed_end = False)

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

