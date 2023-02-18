from flask import Flask, jsonify, url_for, request, redirect, render_template
import config
print(__name__)
app = Flask(__name__)
app.config.from_object(config)

# 图书列表
books = [
    {"b_id": "001",
     "name": "水浒2传",
     "time": "2022.1111111111.1111111111",
     "b_url": "/books_item/?b_id=001"},
    {"b_id": "002",
     "name": "三国演义",
     "time": "2022.2.1111111111",
     "b_url": "/books_item/?b_id=002"}
]


@app.route("/index/")  # 首页
def index():
    return render_template("index.html")


@app.route('/books_list/')  # 图书列表页
def books_list():
    return render_template("books_list.html", books=books)


@app.route('/books_item/')  # 图书详情
def books_item():
    b_id = request.args.get("b_id")
    for i in books:
        if i["b_id"] == b_id:
            return render_template("books_item.html", i=i)


if __name__ == '__main__':
    app.run()
