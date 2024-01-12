# generate_inbetween_values.py
debug_enabled = True

def debug(msg, end='\n'):
    if debug_enabled:
        print(msg, end=end)

# N is number of value total, M is number we want to pick (evenly spaced in N)
def select_values(N, M, closed = True, allow_optimisation = True, is_inner = False):
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

    debug(f"====================== is_inner = {is_inner}")
    debug(f"N: {N} M: {M}")

    # avoid division by zero in degenerate case M = 1
    if M == 1:
        debug(f"Got M = 1, so returning N // 2 = [{N // 2}]")
        return [N // 2]

    if not closed and not is_inner:
    # if not closed:
        # we're not having items at first, last index, so add 2 to M
        print(f" ()() adding 2 to M, now got M = {M}")
        M += 2

    D = (N - 1) // (M - 1)
    debug(f"D: {D}")
    
    # Calculate the remainder to adjust spacing
    R = (N - 1) % (M - 1)
    debug(f"R: {R}")

    S = (M - 1) // R if R > 0 else None
    debug(f"S: {S}")

    # optimisation: start with entire range if there are more values than holes
    if allow_optimisation and D < 2 and R > 0:
        debug(f">>>>>>>>> optimising, because D = {D} (< 2) and R = {R} (> 0)")

        # I was trying this! no worky.
        # new_n = N if closed else N - 2
        # gap_indexes = select_values(new_n, new_n - M, closed = False, is_inner = True)
        # for 4, 3 this is called with 2, 1
        gap_indexes = select_values(N - 2, N - M, closed = False, is_inner = True)

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
    
    values = [0] if closed else []
    
    

    spaces = N - M
    debug(f"spaces: {spaces}")

    # Current value
    current_value = 0

    # every time bump % S == 0 we increment current_value by 1
    bump_index = 0
    
    for idx in range(0, M - 2):
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
        values.append(current_value)
    
    # # Always include N as the last value
    # values.append(N)

    if closed:  
        values.append(N - 1)

    return values


def run(N, M, closed = True, allow_optimisation = True):
    debug("------------------------------------")
    debug("------------------------------------")
    debug("\n")

    result = select_values(N, M, closed, allow_optimisation)

    debug(f"-->> for N: {N}, M: {M}, closed: {closed}, allow_optimisation = {allow_optimisation}: {result}  ", end='')

    # asci repr
    for i in range(N):
        if i in result:
            print("*", end='')
        else:
            print(".", end='')

    print()

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


run(4, 3, closed = False)
run(4, 3, closed = False, allow_optimisation = False)


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

