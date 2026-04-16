# -*- coding: utf-8 -*-
"""
数独 Web 服务：提供 REST API，监听 8081。
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

import sudoku


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
    puzzle = data.get("puzzle")
    solution = data.get("solution")
    if not puzzle or not solution:
        return jsonify({"hint": None, "message": "缺少必要参数"}), 400
    hint = sudoku.get_hint(puzzle, solution)
    if hint:
        return jsonify({"hint": {"row": hint[0], "col": hint[1], "value": hint[2]}})
    return jsonify({"hint": None, "message": "没有空白格子需要提示"})


def run():
    port = int(os.environ.get("PORT", 8081))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    run()
