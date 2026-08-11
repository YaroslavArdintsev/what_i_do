from ReiMekaru import *

# Часть 1
x1, x2, x3, a1, a2, a3, s = syms('x1 x2 x3 a1 a2 a3 s')
init = 4 * x1 ** 2 + 5 * x2 ** 2 + 3 * x3 ** 2 + 5 * x1 * x2 + 2 * x1 * x3 - 2 * x2 * x3 - 16 * x1 - 5 * x2 - 5 * x3
func = function((x1, x2, x3), init)
req1 = -1 * x1 - 3 * x2 + 5 * x3 + 9
req2 = x1 + 2 * x2 - 5 * x3 + 10
req3 = -x1
L = init + a1 * req1 + a2 * req2 + a3 * req3
print('Функция Лагранжа:', L, end='\n\n')

args = [a1, a2, a3, x1, x2, x3]
ds = Ds(L, args)
for d, arg in zip(ds, args):
    print(f'Производная по {arg}: {d}')
print()

sus = Ds_to_zero(L, args)

print('Стационарная точка имеет координаты:', sus)
print('Значение функции в стационарной точке:',
      func(sus[x1], sus[x2], sus[x3]), end='\n\n')
print()

# Часть 2

H = Hesse(ds, args, sus)
minors = corner_minors(H)
print('Матрица Гессе:', H)
print('Угловые миноры матрицы Гессе:', minors)
print(Sylvester(H, 2), end='\n\n')

# Часть 3

J = Jacobi([req1, req2, req3], [x1, x2, x3])
print('Матрица Якоби для всех переменных:', J)
print('Её ранг:', J.rank(), end='\n\n')

S = [x2, x3]
J2 = Jacobi([req1, req2], S)
Jinv = J2.inv()
print('Матрица Якоби для зависимых переменных:', J2)
print('Её определитель:', J2.det())
print('Обратная ей матрица:', Jinv, end='\n\n')

C = Jacobi([req1, req2], x1).T
print('Матрица Якоби для независимых переменных:', C, end='\n\n')

dS = -Jinv * C.T
print('Матрица управления:', dS, end='\n\n')

dX = make_matrix([1, dS[0], dS[1]]).T
print('Изменения переменных при изменении x1 на 1:', dX, end='\n\n')

check = dX * H[2:, 2:] * dX.T
print(float(check[0]), end='\n\n')

# Часть 4

gradS = (Jacobi(init, S) * dS)[0, 0]
print('Градиент по зависимым переменным:', gradS, end='\n\n')

gradX = Jacobi(init, x1)[0, 0] + gradS
print('Приведённый градиент:', gradX, end='\n\n')

eqs2 = [Eq(req1), Eq(req2), Eq(gradX)]
sus2 = solve(eqs2, [x1, x2, x3])
print('Стационарная точка, найденная методом Лагранжа:', sus)
print('Стационарная точка, найденная методом Якоби:', sus2, end='\n\n')

# Часть 5

dgradX = function([x1, x2, x3], D(gradX, x1) + D(gradX, x2)
                  * dS[0] + D(gradX, x3) * dS[1])
print(dgradX(*sus2.values()), end='\n\n')

# Часть 6

b1, b2 = Jacobi(init, S) * Jinv
print(Jacobi(init, S))
print(Jinv)
print('Чувствительность по 1 ограничению:', b1)
print('Чувствительность по 2 ограничению:', b2, end='\n\n')

x1, x2, x3 = sus2.values()
print('Значения чувствительности (Якоби):', eval(str(b1)), eval(str(b2)))
print('Значения чувствительности (Лагранж):', sus[a1], sus[a2])
