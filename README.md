# Reckonsys-latikesh
```sh
python -v 3.10.6
django-admin -v 4.1.2
```
Project Schema

Author
- name

Post
- title
- description
- publish_date
- Author -> Id

Comment
- name
- email
- content
- created
- posts

Following are the Queries and Mutation for graphQL

1. Get all posts
```sh
query {
  posts{
    id
    title
    description
    publishDate
  }
}
```

2. Create Posts
```sh
mutation {
  createPost( title: "This is sample title three" description: "This is sample description", publishDate: "2006-01-02T15:04:05", authorId: 2)
  {
    post{
      title
      description
      publishDate
    }
  }
}
```
3. Update Post
```sh
mutation {
  updatePost(id: 1, title: "Into the mountains and peaks", description: "Sample description"){
    post{
      title
      description
      publishDate
    }
  }
}
```
4. Create Comment
```sh
mutation {
  createComment(name: "Shubham Gadiya", email: "shubham@gmail.com", content:"Sample content", created: "2006-01-02T15:04:05", postId: 1){
    comment{
      name
      email
      content
      created
    }
  }
}
```

5. Delete Comment
```sh
mutation {
  deleteComment(id: 2){
    comment{
      content
    }
  }
}
```

6. Query individual Post
```sh
{
  posts(postId: 2){
    id
    title
    description
  }
}
```
