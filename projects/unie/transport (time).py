from ReiMekaru import *

init = np.array([
[ 6,  7,   8,   9,   8, 100],
[ 5,  6,   7,   8,   6, 75],
[ 4,  6,   7,   8,   7, 100],
[ 3,  5,   6,   7,   8, 150],
[ 5,  6,   7,   8,   6, 100],
[80, 80, 120, 130, 115,   0],
])

times = deepcopy(init)
supplies = init[:-1, -1]
demands = init[-1, :-1]

taus = sorted(np.unique(times[:-1, :-1]))
solution = None
best_tau = None

for tau in taus:
    print(f"Проверяем tau = {tau}")
    ok, cert, allowed = forbidden_rows_check(times[:-1, :-1], supplies, demands, tau)

    if ok:
        print("Порог допустим")
        best_tau = tau
        times[np.where(allowed)] = np.max(times) * 1000
        solution = min_element(times)[0]
        break
    else:
        print("Порог недопустим")
        print("Нарушение:", cert, end='\n\n')

print("\nМинимальное время:", best_tau)
print("\nПлан:\n", solution)