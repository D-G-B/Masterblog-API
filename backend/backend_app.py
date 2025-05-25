
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post about Flask", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post about Python."},
    {"id": 3, "title": "Flask API Development", "content": "Learn how to build APIs with Flask."},
    {"id": 4, "title": "Python Basics", "content": "Understanding the basics of Python programming."},
]


def validate_blogpost_data(data):
    """
    Validates if the incoming blog post data contains 'title' and 'content'.

    :param data: A dictionary containing the blog post data.
    :return: A list of strings representing the names of missing fields (e.g., ['title', 'content']).
             Returns an empty list if all required fields are present.
    """
    missing_fields=[]
    if "title" not in data:
        missing_fields.append("title")
    if "content" not in data:
        missing_fields.append("content")
    return missing_fields


def find_blogpost_by_id(post_id):
    """
    Finds a blog post by its unique ID.

    :param post_id: The integer ID of the blog post to find.
    :return: A dictionary representing the blog post if found, otherwise None.
    """
    return next((post for post in POSTS if post['id']== post_id), None)


def validate_search_queries(sort_by, direction):
    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    if sort_by and sort_by not in valid_sort_fields:
        return False, f"Invalid 'sort field: '{sort_by}'. Must be 'title' or 'content'."
    if direction and direction not in valid_directions:
        return False, f"Invalid direction: '{direction}'. Must be 'asc' or 'desc'"

    return True, None

@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'GET':
        sort_by = request.args.get('sort')
        direction = request.args.get('direction')

        posts_to_return = list(POSTS)

        # First check if sort fields are valid
        validated, error_message = validate_search_queries(sort_by, direction)
        if not validated:
            return jsonify({"error": error_message}), 400

        if sort_by:
            reverse_sort = (direction == 'desc')
            posts_to_return.sort(key=lambda p: p[sort_by].lower(), reverse=reverse_sort)

        return jsonify(posts_to_return)


    else:
        # Handles POST requests to add a new blog post
        new_blog_post = request.get_json()

        # Validate the incoming data
        missing_fields = validate_blogpost_data(new_blog_post)
        if missing_fields:
            error_message = f"Missing required fields: {', '.join(missing_fields)}"
            return jsonify({"error": error_message}), 400

        # Generate a new unique ID for the blog post
        if POSTS:
            new_id = max(post['id'] for post in POSTS) + 1
        else:
            new_id = 1

        new_blog_post['id'] = new_id

        # Add the new post to our list
        POSTS.append(new_blog_post)

        return jsonify(new_blog_post), 201

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global POSTS

    # Find the book to delete with the given ID
    post_to_del = find_blogpost_by_id(id)

    if post_to_del is None:
        return jsonify({"message": "Post not found"}), 404

    # Remove post from POSTS dict
    POSTS = [post for post in POSTS if post['id'] != id]

    return jsonify({"message": f"Post with id - {id} - has been deleted successfully."}), 200

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # Find the post with the given ID
    post = find_blogpost_by_id(id)

    # If post not found, return a 404 error
    if post is None:
        return jsonify({"message": "Post not found"}), 404

    # Update ost with the new_data
    new_data = request.get_json()
    if new_data is not None:
        post.update(new_data)

    return jsonify(post), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    # If neither title nor content params are provided, return empty list
    if not title_query and not content_query:
        return jsonify([])

    # Normalize search terms to lowercase if they exist
    title_query_lower =  title_query.lower() if title_query else None
    content_query_lower = content_query.lower() if content_query else None

    found_posts = []
    for post in POSTS:
        title_matches = False
        content_matches = False

        # Check if  title matches
        if title_query_lower and post.get('title'):
            if title_query_lower in post['title'].lower():
                title_matches = True

        # Check if  content matches
        if content_query_lower and post.get('content'):
            if content_query_lower in post['content'].lower():
                content_matches = True

        if title_matches or content_matches:
            found_posts.append(post)

    found_posts.sort(key=lambda p: p['id'])

    return jsonify(found_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
