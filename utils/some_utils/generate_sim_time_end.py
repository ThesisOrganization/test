incr = 1000

init_sim = 1000
max_sim = 300000

max_sim_taken = max_sim + incr

final_list = list(range(init_sim, max_sim_taken, incr))

print(final_list)

print()


print("(", end="")
for el in final_list:
    print('"' + str(el) + '" ', end="")
print(")")
