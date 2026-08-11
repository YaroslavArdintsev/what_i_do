from ReiMekaru import *


init = np.array([
[23,  13,   12,    8,    22, 40],
[20,  18,   14,   16,    15, 65],
[ 5,   3,   17,   19,     7, 80],
[ 9,  10,   21,    4,    11, 65],
[45,  50,   40,   75,    40,  0],
])

balanced_init, dummy_info = balance_transport_table(init, dummy_cost=0)

print('Сбалансированная таблица:', balanced_init, sep='\n', end='\n\n')
if dummy_info is not None:
    if dummy_info[0] == 'destination':
        print(f'Добавлен фиктивный пункт назначения, столбец {dummy_info[1]}', end='\n\n')
    else:
        print(f'Добавлен фиктивный поставщик, строка {dummy_info[1]}', end='\n\n')

sol, supplies, requests = min_element(balanced_init)
print('Начальный план:', sol, sep='\n', end='\n\n')
basis = build_basis(sol)
basis = complete_basis(sol, basis)

if len(basis) == sol.shape[0] + sol.shape[1] - 1:
    print('Базис построен корректно', end='\n\n')
else:
    raise ValueError('Не удалось дополнить базис!')

while True:
    rows_potentials, cols_potentials = potentials(sol, balanced_init, basis)
    print('Потенциалы строк:', rows_potentials, 'Потенциалы столбцов:', cols_potentials, sep='\n', end='\n\n')

    straffen = np.zeros_like(sol)
    rows, cols = sol.shape
    for row in range(rows):
        for col in range(cols):
            straffen[row][col] = rows_potentials[row] + cols_potentials[col] - balanced_init[row, col]
    print('Штрафы:', straffen, sep='\n', end='\n\n')

    max_el = np.max(straffen)
    if max_el <= 0:
        found = True
        break
    position = np.where(straffen == max_el)
    row_positions, col_positions = position
    positions = [(int(pos1), int(pos2)) for pos1, pos2 in zip(row_positions, col_positions)]
    for pos in positions:
        row, col = pos
        ways = [[(row, col)]]
        basis.append((row, col))
        eurica = None
        show_must_go_on = True
        while show_must_go_on and ways:
            new_ways = []
            for way in ways:
                first = way[0]
                last = way[-1]
                if len(way) % 2 == 0:
                    variants = sol[:, last[1]]
                    if sum((i, last[1]) in basis for i in range(rows)) <= 1:
                        continue
                    for i in range(rows):
                        if i == last[0]:
                            continue
                        new_pos = (i, last[1])
                        if new_pos in basis:
                            if new_pos == first:
                                eurica = way
                                show_must_go_on = False
                                break
                            elif new_pos in way:
                                continue
                            else:
                                new_way = deepcopy(way)
                                new_way.append(new_pos)
                                new_ways.append(new_way)
                else:
                    variants = sol[last[0]]
                    if sum((last[0], j) in basis for j in range(cols)) <= 1:
                        continue
                    for i in range(cols):
                        if i == last[1]:
                            continue
                        new_pos = (last[0], i)
                        if new_pos in basis:
                            if new_pos == first:
                                eurica = way
                                show_must_go_on = False
                                break
                            elif new_pos in way:
                                continue
                            else:
                                new_way = deepcopy(way)
                                new_way.append(new_pos)
                                new_ways.append(new_way)
            ways = deepcopy(new_ways)
        if eurica: break

    if eurica is None: raise ValueError('Решение невозможно!')
    print('Цикл построен:', eurica)

    minus_positions = eurica[1::2]
    minus_values = [sol[pos] for pos in minus_positions]
    min_value = min(minus_values)
    leaving_pos = minus_positions[minus_values.index(min_value)]

    for i, pos in enumerate(eurica):
        sol[pos] += min_value * (-1) ** i

    basis.remove(leaving_pos)

    print('Новая таблица:', sol, sep='\n', end='\n\n')

print('Оптимальный маршрут найден!')
print(sol, end='\n\n')

ans = 0
for i in range(sol.shape[0]):
    for j in range(sol.shape[1]):
        ans += sol[i, j] * init[i, j]
print('Оптимальная стоимость:', ans)