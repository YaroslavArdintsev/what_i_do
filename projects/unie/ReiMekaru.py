from collections.abc import Iterable
from copy import deepcopy
from itertools import combinations
import numpy as np
import sympy as sp

np.set_printoptions(suppress=True)

def syms(args: str):
    return sp.symbols(args)


def function(args, expr):
    return sp.lambdify(args, expr)


def D(expr, arg):
    return sp.diff(expr, arg)


def Ds(expr, args):
    return [D(expr, arg) for arg in args]


def Eq(expr, res=0):
    return sp.Eq(expr, res)


def solve(eqs, args):
    return sp.solve(eqs, args)


def Ds_to_zero(expr, args):
    return solve([Eq(d) for d in Ds(expr, args)], args)


def make_matrix(els):
    return sp.Matrix(els)


def Hesse(ds, args, dot):
    xs = dot.values()
    return make_matrix([[function(args, sp.diff(d, arg))(*xs) for arg in args] for d in ds])


def corner_minors(matrix):
    return [matrix[:i, :i].det() for i in range(1, min(matrix.shape) + 1)]


def Sylvester(matrix, M=0):
    mins = corner_minors(matrix)[2*M:]
    if all(min > 0 for min in mins):
        end = 'положительно определена'
    elif all(min * (-1) ** pos < 0 for pos, min in enumerate(mins)):
        end = 'отрицательно определена'
    else:
        end = 'не определена'
    return f'Квадратичная форма {end}'


def Jacobi(exprs, args):
    if not isinstance(args, Iterable):
        el, args = args, []
        args.append(el)
    if not isinstance(exprs, Iterable):
        elem, exprs = exprs, []
        exprs.append(elem)
    return make_matrix([[D(expr, arg) for arg in args] for expr in exprs])


def is_unit_for_row(A, j, i, tol=1e-9):
    col = A[:, j]
    if not np.isclose(col[i], 1.0, atol=tol):
        return False
    for r in range(len(col)):
        if r != i and not np.isclose(col[r], 0.0, atol=tol):
            return False
    return True


def find_initial_basis(A, columns):
    m, n = A.shape
    basis = [None] * m
    used_cols = set()

    for i in range(m):
        for j in range(n):
            if j in used_cols:
                continue
            if is_unit_for_row(A, j, i):
                basis[i] = columns[j]
                used_cols.add(j)
                break

    return basis


def add_artificial_variables(table, columns, method='DoublePhase'):
    A = table[:-1, :-1].copy()
    b = table[:-1, -1].copy()
    z = table[-1].copy()
    z_rhs = table[-1, -1].copy()

    m, n = A.shape
    basis = find_initial_basis(A, columns[:-1])
    artificial_cols = []
    artificial_names = []

    for i in range(m):
        if basis[i] is None:
            new_col = np.zeros((m, 1))
            new_col[i, 0] = 1.0
            A = np.hstack((A, new_col))

            a_name = f'a{i + 1}'
            artificial_names.append(a_name)
            artificial_cols.append(A.shape[1] - 1)

            basis[i] = a_name

    new_columns = columns[:-1] + artificial_names + ['СЧ']
    if method == 'DoublePhase':
        new_z = np.zeros(A.shape[1])

        for j in artificial_cols:
            new_z[j] = 1

        new_A = np.hstack((A, b.reshape(-1, 1)))
        new_z = np.hstack((new_z, np.array([z_rhs])))

    elif method == 'M':
        M = 100 * np.max(np.abs(table))
        new_z = np.hstack((z, np.zeros(len(artificial_cols))))

        for j in artificial_cols:
            new_z[j] = M

        new_A = np.hstack((A, b.reshape(-1, 1)))

    for i in range(len(new_A)):
        if 'a' in basis[i]:
            value = M * new_A[i] if method == 'M' else new_A[i]
            new_z -= value

    new_table = np.vstack((
        new_A,
        new_z
    ))

    rows = basis + ['z']
    return new_table, new_columns, rows, artificial_names, artificial_cols, z


def simplex_step(table, rows, columns):
    stop = -1
    for i in range(len(columns)):
        if 'a' in columns[i]:
            stop = i
            break

    last_row = table[-1, :stop]
    el = last_row.min()

    if el >= 0:
        return table, rows, False

    print('Отрицательный элемент найден:', el)
    index2 = np.where(np.isclose(last_row, el))[0][0]
    print('Его индекс:', index2 + 1, f'({columns[index2]})')

    checker = np.array([
        row[-1] / row[index2] if row[index2] > 0 else np.inf
        for row in table[:-1]
    ])

    if np.all(np.isinf(checker)):
        raise ValueError("Задача неограничена: в ведущем столбце нет положительных элементов")

    min_ratio = checker.min()
    print('Минимальное частное:', min_ratio)
    index1 = np.where(np.isclose(checker, min_ratio))[0][0]
    print('Его индекс:', index1 + 1, f'({rows[index1]})')

    pivot = table[index1, index2]
    table[index1] = table[index1] / pivot

    for i in range(table.shape[0]):
        if i != index1:
            table[i] = table[i] - table[index1] * table[i, index2]

    rows[index1] = columns[index2]

    print('Обновленная таблица:\n', table, end='\n\n')
    return table, rows, True


def dva_simplex_step(table, rows, columns):
    last_col = table[:-1, -1]
    el = last_col.min()

    if el >= 0:
        return table, rows, False

    print('Отрицательный элемент найден:', el)
    index1 = np.where(np.isclose(last_col, el))[0][0]
    print('Его индекс:', index1 + 1, f'({rows[index1]})')

    checker = np.array([
        col[-1] / col[index1] if col[index1] < 0 else np.inf
        for col in table[:, :-1].T
    ])

    if np.all(np.isinf(checker)):
        raise ValueError("Задача неограничена: в ведущем столбце нет отрицательных элементов")

    min_ratio = checker.min()
    print('Минимальное частное:', min_ratio)
    index2 = np.where(np.isclose(checker, min_ratio))[0][0]
    print('Его индекс:', index2 + 1, f'({columns[index2]})')

    pivot = table[index1, index2]
    table[index1] = table[index1] / pivot

    for i in range(table.shape[0]):
        if i != index1:
            table[i] = table[i] - table[index1] * table[i, index2]

    rows[index1] = columns[index2]

    print('Обновленная таблица:\n', table, end='\n\n')
    return table, rows, True


def balance_transport_table(table, dummy_cost=0):
    prices = table[:-1, :-1].copy()
    supplies = table[:-1, -1].copy()
    requests = table[-1, :-1].copy()

    sum_supplies = supplies.sum()
    sum_requests = requests.sum()

    if np.isclose(sum_supplies, sum_requests):
        return table.copy(), None

    rows, cols = prices.shape

    if sum_supplies > sum_requests:
        diff = sum_supplies - sum_requests
        dummy_col = np.full((rows, 1), dummy_cost, dtype=table.dtype)
        prices = np.hstack((prices, dummy_col))
        requests = np.append(requests, diff)
        dummy_info = ('destination', cols)
    else:
        diff = sum_requests - sum_supplies
        dummy_row = np.full((1, cols), dummy_cost, dtype=table.dtype)
        prices = np.vstack((prices, dummy_row))
        supplies = np.append(supplies, diff)
        dummy_info = ('source', rows)

    balanced = np.zeros((prices.shape[0] + 1, prices.shape[1] + 1), dtype=table.dtype)
    balanced[:-1, :-1] = prices
    balanced[:-1, -1] = supplies
    balanced[-1, :-1] = requests

    return balanced, dummy_info


def transform_table(table):
    requests = deepcopy(table[-1, :-1])
    supplies = deepcopy(table[:-1, -1])
    new_table = np.zeros_like(table)
    new_table[-1, :-1] = requests
    new_table[:-1, -1] = supplies
    return new_table, supplies, requests


def north_west(table):
    new_table, supplies, requests = transform_table(table)
    row, col = 0, 0
    while supplies[-1] > 0 and requests[-1] > 0:
        el = min(supplies[row], requests[col])
        new_table[row, col] = el
        supplies[row] -= el
        requests[col] -= el
        if supplies[row] == 0:
            row += 1
        if requests[col] == 0:
            col += 1
    return new_table[:-1, :-1], supplies, requests


def min_element(table):
    new_table, supplies, requests = transform_table(table)
    prices = deepcopy(table[:-1, :-1])
    maxim = np.max(prices) + 1
    while sum(supplies) > 0 and sum(requests) > 0:
        pos = np.where(prices == np.min(prices))
        row = pos[0][0]
        col = pos[1][0]
        el = min(supplies[row], requests[col])
        new_table[row, col] = el
        supplies[row] -= el
        requests[col] -= el
        if supplies[row] == 0:
            prices[row] = np.array([maxim for _ in range(len(supplies))])
        if requests[col] == 0:
            prices[:, col] = np.array([maxim for _ in range(len(requests))])
    return new_table[:-1, :-1], supplies, requests


def Vogel(table):
    new_table, supplies, requests = transform_table(table)
    prices = deepcopy(table[:-1, :-1])
    maxim = np.max(prices) + 1
    while sum(supplies) > 0 and sum(requests) > 0:
        straffen = [sorted(prices[row])[1] - sorted(prices[row])[0] for row in range(len(supplies))]
        straffen.extend([sorted(prices[:, col])[1] - sorted(prices[:, col])[0] for col in range(len(requests))])
        pos = np.where(straffen == np.max(straffen))[0][0]
        if pos - len(supplies) >= 0:
            col = pos - len(supplies)
            row = np.where(prices[:, col] == np.min(prices[:, col]))[0][0]
        else:
            row = pos
            col = np.where(prices[row] == np.min(prices[row]))[0][0]
        el = min(supplies[row], requests[col])
        new_table[row, col] = el
        supplies[row] -= el
        requests[col] -= el
        if supplies[row] == 0:
            prices[row] = np.array([maxim for _ in range(len(supplies))])
        if requests[col] == 0:
            prices[:, col] = np.array([maxim for _ in range(len(requests))])
    return new_table[:-1, :-1], supplies, requests


def build_basis(sol):
    basis1, basis2 = np.where(sol != 0)
    basis = list(zip(map(int, basis1), map(int, basis2)))
    return basis


def complete_basis(sol, basis):
    rows, cols = sol.shape
    need = rows + cols - 1
    if len(basis) >= need:
        return basis

    basis_set = set(basis)
    parent = list(range(rows + cols))
    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    def union(v1, v2):
        p1, p2 = find(v1), find(v2)
        if p1 != p2:
            parent[p2] = p1
            return True
        return False

    for r, c in basis_set:
        union(r, rows + c)

    for r in range(rows):
        for c in range(cols):
            pos = (r, c)
            if pos in basis_set:
                continue
            if union(r, rows + c):
                basis.append(pos)
                basis_set.add(pos)
                if len(basis) == need:
                    return basis

    return basis


def potentials(table, prices, basis):
    rows, cols = table.shape
    equations = np.zeros([rows + cols, rows + cols])
    solutions = np.zeros(rows + cols)
    equations[0, 0] = 1
    num = 0
    for row in range(rows):
        for col in range(cols):
            if (row, col) in basis:
                num += 1
                equations[num, row] = 1
                equations[num, rows + col] = 1
                solutions[num] = prices[row, col]
    solution = np.linalg.solve(equations, solutions)
    row_potentials, col_potentials = solution[:rows], solution[rows:]
    return row_potentials, col_potentials


def forbidden_rows_check(times, supplies, demands, tau):
    allowed = times <= tau
    m, n = allowed.shape

    for r in range(1, m + 1):
        for subset in combinations(range(m), r):
            subset = list(subset)
            supply_sum = supplies[subset].sum()
            reachable_cols = np.where(np.any(allowed[subset, :], axis=0))[0]
            demand_sum = demands[reachable_cols].sum()

            if supply_sum > demand_sum:
                return False, {
                    "rows": subset,
                    "cols": reachable_cols.tolist(),
                    "supply_sum": int(supply_sum),
                    "demand_sum": int(demand_sum),
                }, allowed

    return True, None, allowed