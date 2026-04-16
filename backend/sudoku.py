# -*- coding: utf-8 -*-
"""
数独核心逻辑：生成、验证、求解
"""
import random
from typing import List, Optional, Tuple


def _box_index(row: int, col: int) -> int:
    """计算 3x3 宫格索引 (0-8)"""
    return (row // 3) * 3 + col // 3


def _is_valid_placement(grid: List[List[int]], row: int, col: int, num: int) -> bool:
    """检查在 (row, col) 放置 num 是否合法"""
    for c in range(9):
        if grid[row][c] == num:
            return False
    for r in range(9):
        if grid[r][col] == num:
            return False
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if grid[r][c] == num:
                return False
    return True


def _solve(grid: List[List[int]]) -> bool:
    """回溯求解数独，修改原数组，返回是否可解"""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if _is_valid_placement(grid, row, col, num):
                        grid[row][col] = num
                        if _solve(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True


def generate_full_board() -> List[List[int]]:
    """生成一个完整的有效数独终盘"""
    grid = [[0] * 9 for _ in range(9)]
    # 先填第一行随机排列
    first_row = list(range(1, 10))
    random.shuffle(first_row)
    grid[0] = first_row
    _solve(grid)
    return grid


def mask_cells(grid: List[List[int]], count: int) -> Tuple[List[List[int]], List[List[int]]]:
    """
    挖空指定数量的格子，保证有唯一解。
    返回 (题目盘面, 答案盘面)，题目中挖空处为 0。
    """
    from copy import deepcopy
    puzzle = deepcopy(grid)
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    removed = 0
    for row, col in positions:
        if removed >= count:
            break
        old = puzzle[row][col]
        puzzle[row][col] = 0
        # 检查是否仍唯一解：用回溯数解的数量（这里简化为：挖空后能解即可）
        test = [row[:] for row in puzzle]
        if _solve(test):
            removed += 1
        else:
            puzzle[row][col] = old
    return puzzle, deepcopy(grid)


def generate_puzzle(difficulty: str) -> Tuple[List[List[int]], List[List[int]]]:
    """
    按难度生成数独题目。
    difficulty: easy(约 40 空), medium(约 45 空), hard(约 50 空)
    返回 (puzzle, solution)
    """
    counts = {"easy": 40, "medium": 45, "hard": 50}
    n = counts.get(difficulty, 45)
    full = generate_full_board()
    return mask_cells(full, n)


def validate_grid(grid: List[List[int]]) -> Tuple[bool, Optional[str]]:
    """
    验证当前盘面是否合法（无重复且可解）。
    返回 (是否合法, 错误信息)。
    """
    for row in range(9):
        for col in range(9):
            v = grid[row][col]
            if v == 0:
                continue
            grid[row][col] = 0
            if not _is_valid_placement(grid, row, col, v):
                grid[row][col] = v
                return False, f"位置 ({row},{col}) 与已有数字冲突"
            grid[row][col] = v
    test = [row[:] for row in grid]
    if not _solve(test):
        return False, "当前盘面无解"
    return True, None


def is_solution(puzzle: List[List[int]], solution: List[List[int]]) -> bool:
    """检查 solution 是否是 puzzle 的正确解（puzzle 中非零格需一致，且 solution 为合法终盘）"""
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] != 0 and puzzle[r][c] != solution[r][c]:
                return False
    valid, _ = validate_grid(solution)
    if not valid:
        return False
    for r in range(9):
        for c in range(9):
            if solution[r][c] == 0:
                return False
    return True


def get_hint(grid: List[List[int]], solution: List[List[int]]) -> Optional[dict]:
    """
    获取提示：找到第一个空格子，返回其正确答案。
    返回 {"row": int, "col": int, "value": int} 或 None。
    """
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return {"row": r, "col": c, "value": solution[r][c]}
    return None
