from fractions import Fraction

from ReiMekaru import *

'''columns = ['x1', 'x2', 's1', 's2', 's3', 's4', 'СЧ']
table = np.array([
    [1, 1, -1, 0, 0, 0, 4],
    [1, 0, 0, -1, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 6],
    [1, -1, 0, 0, 0, -1, 0],
    [10, 5, 0, 0, 0, 0, 0]
], dtype=float)'''

'''columns = ['x1', 'x2', 's1', 's2', 'СЧ']
table = np.array([
    [4, 5, -1, 0, 1],
    [6, 1, 0, -1, 1],
    [1, 1, 0, 0, 0]
], dtype=float)'''

'''columns = ['x1', 'x2', 's1', 's2', 'СЧ']
table = np.array([
    [1, 3, -1, 0, 1],
    [2, 1, 0, -1, 1],
    [1, 1, 0, 0, 0]
], dtype=float)'''

columns = ['x1', 'x2', 's1', 's2', 'СЧ']
table = np.array([
    [8, 6, -1, 0, 1],
    [7, 8, 0, -1, 1],
    [1, 1, 0, 0, 0]
], dtype=float)

print('Начальная таблица:\n', table, end='\n\n')

rows = find_initial_basis(table[:-1, :-1], columns)
if None in rows:
    for row, value in enumerate(rows):
        if value is None: table[row] *= -1
    table[-1] *= -1
    print('Новая таблица:\n', table, end='\n\n')
rows = find_initial_basis(table[:-1, :-1], columns)

show_must_go_on = True
while show_must_go_on:
    table, rows, show_must_go_on = dva_simplex_step(table, rows, columns)
rows.append('z')
texts = []
for name, value in zip(rows, table[:, -1]):
    frac = Fraction(value).limit_denominator()
    if frac.denominator == 1:
        val_str = str(frac.numerator)
    else:
        val_str = f"{frac.numerator}/{frac.denominator}"
    texts.append(f'{name} = {val_str}' if name != 'z' else f'{name} = {val_str}')
print('Оптимальные значения найдены:', *texts, sep='\n')