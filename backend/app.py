# -*- coding: utf-8 -*-
"""
数独 Web 服务：提供 REST API 与前端页面，监听 8081。
前后端分离架构，后端提供 /api/* 接口。
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

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
        return jsonify({"valid": False, "message": "无效的盘面"}), 400
    if not solution or len(solution) != 9 or any(len(row) != 9 for row in solution):
        return jsonify({"valid": False, "message": "无效的答案"}), 400
    hint = sudoku.get_hint(grid, solution)
    if hint:
        return jsonify({"valid": True, "row": hint["row"], "col": hint["col"], "value": hint["value"]})
    return jsonify({"valid": False, "message": "没有可用提示"})


def run():
    port = int(os.environ.get("PORT", 8081))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    run()
