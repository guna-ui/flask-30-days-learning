from flask import Flask,jsonify, request

app=Flask(__name__)

books_list = [
    {"id": 1, "title": "The Hitchhiker's Guide to the Galaxy", "author_id": 1, "isbn": "978-0345391803", "publication_year": 1979},
    {"id": 2, "title": "1984", "author_id": 2, "isbn": "978-0451524935", "publication_year": 1949}
]

authors_list = [
    {"id": 1, "name": "Douglas Adams", "bio": "English author, screenwriter, and humorist."},
    {"id": 2, "name": "George Orwell", "bio": "English novelist, essayist, journalist, and critic."}
]

users_list = [
    {"id": 1, "username": "user1", "email": "user1@example.com"},
    {"id": 2, "username": "user2", "email": "user2@example.com"}
]

@app.route('/')
def welcome():
    return jsonify({"messagee":"Welcome to personal library"})

@app.route('/test/users')
def users():
    return jsonify(users_list)

@app.route('/test/books')
def books():
    return jsonify(books_list)

@app.route('/test/authors')
def authors():
    return jsonify(authors_list)

@app.route('/books')
def get_books():
    return jsonify({"books":books_list})

def find_item_by_id(itemlist,item_id):
    return next((item for item in itemlist if item['id']==item_id),None)

@app.route('/books/<int:book_id>',methods=['GET'])
def get_singlebook(book_id):
    book_id=find_item_by_id(books_list,book_id)
    if book_id:
        return jsonify({"book":book_id})
    return jsonify({"message": "book not found"}),404

@app.route('/authors')
def get_authors():
    return jsonify({"authors":authors_list})

@app.route('/authors/<int:author_id>')
def get_selected_author(author_id):
    selected_author= find_item_by_id(authors_list,author_id)
    if selected_author:
        return jsonify({"author":selected_author})
    return jsonify({"message":"searched author not available"})

@app.route('/users')
def get_users():
    return jsonify({"users":users})

@app.route('/users/<int:user_id>')
def get_selected_user(user_id):
    selected_user =  find_item_by_id(users_list,user_id)
    if selected_user:
         return jsonify({"selected_user":selected_user})
    return jsonify({"message":"searched user not available"})

@app.route('/books',methods=['POST'])
def create_book():
    data=request.get_json()
    if not data or 'title' not in data or 'author_id' not in data:
        return jsonify({"Message":"Invalid request. Title and Author_id are required"}),404
    
    if not isinstance(data['author_id'],int):
        return jsonify({"message":"Author with that ID not found"}),400
    
    new_book={
        "id": len(books_list) + 1,
        "title" : data['title'],
        "author_id": data["author_id"],
        "isbn"     : data.get('isbn',None),
        "publication_year": data.get('publication_year',None)
    }
    books_list.append(new_book)
    return jsonify({"book": new_book}),201

@app.route('/authors',methods=['POST'])
def create_author():
    data=request.get_json()
    if not data or 'name' not in data or 'bio' not in data:
        return jsonify({"message":"Invalid request. Name and bio are required"}),404
    new_author={
        "id":len(authors_list)+1,
        "name" : data['name'],
        "bio"  : data['bio']
    }
    authors_list.append(new_author)
    return jsonify({"authors":new_author}),201

@app.route('/users',methods=['POST'])
def create_user():
    data=request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"message":"invalid request "}),404
    new_user={
         "id":len(users_list)+1,
         "username": data['username'],
         "email": data['email']
    }
    users_list.append(new_user)
    return jsonify({"users":new_user}),201

if __name__=='__main__':
    app.run(debug=True)