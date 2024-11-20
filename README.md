# fast_api_pro
Social Media post API
@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):

    cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    return {"data": new_post}

when you run the above code psycopg2 throws ProgrammingError. Beacuse Insert statement doesnot return anything,
cursor.fetchone() throws error. To avoid this add RETURNING to the query.