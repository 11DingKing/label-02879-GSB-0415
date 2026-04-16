# -*- coding: utf-8 -*-
"""
数独 Web 服务：提供 API 与前端页面，监听 8081。
"""
import json
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder="static", static_url_path="")

# 确保从 backend 目录加载 sudoku 模块
import sudoku


@app.route("/")
def index():
    return send_from_directory(app.static_folder or ".", "index.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json() or {}
    difficulty = data.get("difficulty", "medium")
    if difficulty not in ("easy", "medium", "hard"):
        difficulty = "medium"
    puzzle, solution = sudoku.generate_puzzle(difficulty)
    return jsonify({"puzzle": puzzle, "solution": solution})


@app.route("/api/validate", methods=["POST"])
def api_validate():
    data = request.get_json() or {}
    grid = data.get("grid")
    if not grid or len(grid) != 9 or any(len(row) != 9 for row in grid):
        return jsonify({"valid": False, "message": "无效的盘面"}), 400
    valid, message = sudoku.validate_grid(grid)
    return jsonify({"valid": valid, "message": message or ""})


@app.route("/api/hint", methods=["POST"])
def api_hint():
    data = request.get_json() or {}
    grid = data.get("grid")
    solution = data.get("solution")
    if not grid or len(grid) != 9 or any(len(row) != 9 for row in grid):
        return jsonify({"success": False, "message": "无效的盘面"}), 400
    if not solution or len(solution) != 9 or any(len(row) != 9 for row in solution):
        return jsonify({"success": False, "message": "缺少答案信息"}), 400
    
    # 找到第一个空白格子
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return jsonify({
                    "success": True,
                    "row": r,
                    "col": c,
                    "value": solution[r][c]
                })
    
    return jsonify({"success": False, "message": "没有空白格子需要提示"})


def run():
    port = int(os.environ.get("PORT", 8081))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    run()
