from ReiMekaru import *

columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 'СЧ']
max_min = 'min'
max_min_dict = {'max': 1, 'min': -1}
table = np.array([
    [1,  1, -1,  0,  0,  0, 4],
    [1, 0,  0, -1,  0,  0, 1],
    [0,  1,  0,  0,  1,  0, 6],
    [1, -1,  0,  0,  0, -1, 0],
    [10, 5,  0,  0,  0,  0, 0]
], dtype=float)
print('Начальная таблица:\n', table, end='\n\n')

new_table, new_columns, rows, artificial_names, artificial_cols, z = add_artificial_variables(table, columns, method='M')

print('Новая таблица:', new_table, 'Столбцы:', new_columns, 'Строки:', rows, sep='\n', end='\n\n')

show_must_go_on = True
while show_must_go_on:
    new_table, rows, show_must_go_on = simplex_step(new_table, rows, new_columns)
texts = (f'{name} = {value}' if name != 'z' else f'{name} = {max_min_dict[max_min] * value}'
         for name, value in zip(rows, new_table[:, -1]))
print('Оптимальные значения найдены:', *texts, sep='\n')