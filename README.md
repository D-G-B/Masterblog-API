# Masterblog API

This is a simple RESTful API for managing blog posts, built with Flask.

## Features

* **Get all posts:** Retrieve a list of all blog posts, with optional sorting.
* **Add a new post:** Create a new blog post with a title and content.
* **Delete a post:** Remove an existing blog post by its ID.
* **Update a post:** Modify the title or content of an existing blog post.
* **Search posts:** Find posts by keywords in their title or content.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Masterblog-API
    ```
    (Replace `<repository_url>` with the actual URL of your repository.)

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python3 backend/backend_app.py
    ```

The API will be available at `http://localhost:5002`.