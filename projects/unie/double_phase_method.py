from ReiMekaru import *

max_min_dict = {'max': 1, 'min': -1}

columns = ['x1', 'x2', 's1', 's2', 'СЧ']
max_min = 'min'
table = np.array([
    [8, 6, -1, 0, 1],
    [7, 8, 0, -1, 1],
    [1, 1, 0, 0, 0]
], dtype=float)

#Двойственный симплекс-метод

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 'СЧ']
max_min = 'min'
table = np.array([
    [1, 1, -1, 0, 0, 0, 4],
    [1, 0, 0, -1, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 6],
    [1, -1, 0, 0, 0, -1, 0],
    [10, 5, 0, 0, 0, 0, 0]
], dtype=float)'''

#Метод Гомори

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 'СЧ']
max_min = 'min'
table = np.array([
    [1, 2, -1, 0, 0, 0, 7],
    [1, 0, 0, -1, 0, 0, 2],
    [0, 1, 0, 0, 1, 0, 6],
    [1, -1, 0, 0, 0, -1, 3],
    [10, 15, 0, 0, 0, 0, 0]
], dtype=float)'''

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 's5', 'СЧ']
max_min = 'min'
table = np.array([
    [1, 2, -1, 0, 0, 0, 0, 7],
    [1, 0, 0, -1, 0, 0, 0, 2],
    [0, 1, 0, 0, 1, 0, 0, 6],
    [1, -1, 0, 0, 0, -1, 0, 3],
    [0, 0, 1, 0, 0, 2, -1, 2],
    [10, 15, 0, 0, 0, 0, 0, 0]
], dtype=float)'''

#Компромиссное решение

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 'СЧ']
max_min = 'max'
table = np.array([
    [8, 12, 1, 0, 0, 0, 48],
    [12, 6, 0, 1, 0, 0, 36],
    [1, 0, 0, 0, 1, 0, 4],
    [0, 1, 0, 0, 0, -1, 2],
    [-1, -3, 0, 0, 0, 0, 0]
], dtype=float)'''

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 'СЧ']
max_min = 'min'
table = np.array([
    [8, 12, 1, 0, 0, 0, 48],
    [12, 6, 0, 1, 0, 0, 36],
    [1, 0, 0, 0, 1, 0, 4],
    [0, 1, 0, 0, 0, -1, 2],
    [2, 1, 0, 0, 0, 0, 0]
], dtype=float)'''

'''columns = ['x1', 'x2', 'z', 's1', 's2', 's3', 's4', 's5', 's6', 'СЧ']
max_min = 'min'
table = np.array([
    [8, 12, 0, 1, 0, 0, 0, 0, 0, 48],
    [12, 6, 0, 0, 1, 0, 0, 0, 0, 36],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 4],
    [0, 1, 0, 0, 0, 0, -1, 0, 0, 2],
    [1, 3, 12, 0, 0, 0, 0, -1, 0, 12],
    [2, 1, -2, 0, 0, 0, 0, 0, 1, 2],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
], dtype=float)'''

#Метод последовательных уступок I

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 's5', 'СЧ']
max_min = 'min'
table = np.array([
    [8, 12, 1, 0, 0, 0, 0, 48],
    [12, 6, 0, 1, 0, 0, 0, 36],
    [1, 0, 0, 0, 1, 0, 0, 4],
    [0, 1, 0, 0, 0, -1, 0, 2],
    [1, 3, 0, 0, 0, 0, -1, 12 * 0.9],
    [2, 1, 0, 0, 0, 0, 0, 0]
], dtype=float)'''

#Метод последовательных уступок II

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 's5', 'СЧ']
max_min = 'min'
z = 0.95
table = np.array([
    [8, 12, 1, 0, 0, 0, 0, 48],
    [12, 6, 0, 1, 0, 0, 0, 36],
    [1, 0, 0, 0, 1, 0, 0, 4],
    [0, 1, 0, 0, 0, -1, 0, 2],
    [1, 3, 0, 0, 0, 0, -1, 12 * z],
    [2, 1, 0, 0, 0, 0, 0, 0]
], dtype=float)'''

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 's5', 'СЧ']
max_min = 'max'
z = 1.1
table = np.array([
    [8, 12, 1, 0, 0, 0, 0, 48],
    [12, 6, 0, 1, 0, 0, 0, 36],
    [1, 0, 0, 0, 1, 0, 0, 4],
    [0, 1, 0, 0, 0, -1, 0, 2],
    [2, 1, 0, 0, 0, 0, 1, 2 * z],
    [-1, -3, 0, 0, 0, 0, 0, 0]
], dtype=float)'''

#Метод равных отклонений

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 'СЧ']
max_min = 'max'
table = np.array([
    [8, 12, 1, 0, 0, 0, 48],
    [12, 6, 0, 1, 0, 0, 36],
    [1, 0, 0, 0, 1, 0, 4],
    [0, 1, 0, 0, 0, -1, 2],
    [13/12, 3/4, 0, 0, 0, 0, 2],
    [-1, -3, 0, 0, 0, 0, 0]
], dtype=float)'''

#Метод экспертных оценок

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 'СЧ']
max_min = 'max'
a1 = 0.4
a2 = 0.6
table = np.array([
    [8, 12, 1, 0, 0, 0, 48],
    [12, 6, 0, 1, 0, 0, 36],
    [1, 0, 0, 0, 1, 0, 4],
    [0, 1, 0, 0, 0, -1, 2],
    [-(a1/12 - a2), -(a1/4 - a2/2), 0, 0, 0, 0, 0]
], dtype=float)'''

print('Начальная таблица:\n', table, end='\n\n')

print('Этап 1', end='\n\n')

new_table, new_columns, rows, artificial_names, artificial_cols, z = add_artificial_variables(table, columns)

print('Таблица:', new_table, 'Столбцы:', new_columns, 'Строки:', rows, sep='\n', end='\n\n')

show_must_go_on = True
while show_must_go_on:
    new_table, rows, show_must_go_on = simplex_step(new_table, rows, new_columns)

if not np.isclose(new_table[-1, -1], 0):
    raise ValueError('Задача недопустима!')
else:
    print('Целевая функция равна 0', end='\n\n')

print('Этап 2', end='\n\n')

for a, pos in zip(artificial_names[::-1], artificial_cols[::-1]):
    new_columns.remove(a)
    new_table = np.delete(new_table, pos, axis=1)
new_table[-1] = z
print('Таблица:', new_table, 'Столбцы:', new_columns, 'Строки:', rows, sep='\n', end='\n\n')

for i in range(len(new_columns)):
    if new_columns[i] in rows and new_table[-1, i] != 0:
        j = rows.index(new_columns[i])
        new_table[-1] -= new_table[j] * new_table[-1, i] / new_table[j, i]
print(new_table, end='\n\n')

show_must_go_on = True
while show_must_go_on:
    new_table, rows, show_must_go_on = simplex_step(new_table, rows, new_columns)
for num, result in enumerate(new_table[:, -1]):
    for i in range(4):
        if np.isclose(result, round(result, i)):
            new_table[num, -1] = round(result, i)
            break
texts = (f'{name} = {value}' if name != 'z' else f'{name} = {max_min_dict[max_min] * value}'
         for name, value in zip(rows, new_table[:, -1]))
print('Оптимальные значения найдены:', *texts, sep='\n')