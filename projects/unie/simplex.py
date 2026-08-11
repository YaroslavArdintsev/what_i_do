from ReiMekaru import *

columns = ['x1', 'x2', 's1', 's2', 's3', 'СЧ']
max_min = 'min'
max_min_dict = {'max': 1, 'min': -1}
table = np.array([
    [-2, 1, 1, 0, 0, 2],
    [1, -2, 0, 1, 0, 2],
    [1,  1, 0, 0, 1, 5],
    [-1, 1, 0, 0, 0, 0]
], dtype=float)

print('Начальная таблица:\n', table, end='\n\n')

rows = find_initial_basis(table[:-1, :-1], columns)

show_must_go_on = True
while show_must_go_on:
    table, rows, show_must_go_on = simplex_step(table, rows, columns)
rows.append('z')
texts = (f'{name} = {value}' if name != 'z' else f'{name} = {max_min_dict[max_min] * value}'
         for name, value in zip(rows, table[:, -1]))
print('Оптимальные значения найдены:', *texts, sep='\n')