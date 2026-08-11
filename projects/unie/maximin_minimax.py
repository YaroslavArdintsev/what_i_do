from ReiMekaru import *

game = np.array([
[7, 7, 8],
[6, 8, 7],
[12, 10, 11],
[5, 8, 8],
[7, 7, 10],
[11, 8, 10]
])

A = [np.min(game[i]) for i in range(game.shape[0])]
B = [np.max(game[:, i]) for i in range(game.shape[1])]

win_A = np.max(A)
win_B = np.min(B)

if win_A != win_B:
    raise ValueError('Ошибка! Игру нужно решать в смешанных стратегиях!')
print(f'Цена игры: {win_A}',
      f'Оптимальная стратегия первого игрока: {np.where(A==win_A)[0][0] + 1}',
      f'Оптимальная стратегия второго игрока: {np.where(B==win_B)[0][0] + 1}', sep='\n')