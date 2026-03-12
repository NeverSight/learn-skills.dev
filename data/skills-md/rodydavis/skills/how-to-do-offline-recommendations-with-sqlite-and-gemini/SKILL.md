---
name: how-to-do-offline-recommendations-with-sqlite-and-gemini
description: Learn how to enhance your CMS like PocketBase with AI-powered content recommendations using text embeddings, SQLite, and k-nearest neighbor search for efficient and scalable related content suggestions.
metadata:
  url: https://rodydavis.com/posts/offline-vector-recommendations
  last_modified: Tue, 03 Feb 2026 20:04:15 GMT
---

# How to do Offline Recommendations with SQLite and Gemini


When working with a CMS (like [PocketBase](https://pocketbase.io)) it is common to add some sort of recommendatios for related content. For example you can have a list of blog posts, and show related posts either by random selection or recently viewed.  
  
I first learned about this technique from [Aaron Francis](https://aaronfrancis.com) on his YouTube channel:

## Text Embeddings

[Text embeddings](https://ai.google.dev/gemini-api/docs/embeddings) are a way to convert a chunk of text into a an array of numbers. Having a mathematical representation means we can easily store them in a database and run common functions to calculate the distances between vectors that we have stored.

> You will need an [API Key from AI Studio](https://aistudio.google.com/apikey) to generate the descriptions and embeddings.

In order to create the embedding we need to first generate chunk small enough to fit in the embedding window size. For example we can use an LLM like [Gemini to generate a description](https://ai.google.dev/gemini-api/docs/text-generation?lang=go) for a blog post and then vectorize the description which we can store in the database.

> We only need to generate a new embedding and description when the content changes which limits the billing costs to the frequency of the content changes.

## Storing the Vectors

To store the text embeddings as vectors we can save them in a [SQLite](https://www.sqlite.org) database using a [runtime loadable extension](https://www.sqlite.org/loadext.html) called [sqlite-vec](https://github.com/asg017/sqlite-vec). Here is an example from the readme on how to query the vectors directly in SQLite:

```
.load ./vec0

create virtual table vec_examples using vec0(
  sample_embedding float[8]
);

-- vectors can be provided as JSON or in a compact binary format
insert into vec_examples(rowid, sample_embedding)
  values
    (1, '[-0.200, 0.250, 0.341, -0.211, 0.645, 0.935, -0.316, -0.924]'),
    (2, '[0.443, -0.501, 0.355, -0.771, 0.707, -0.708, -0.185, 0.362]'),
    (3, '[0.716, -0.927, 0.134, 0.052, -0.669, 0.793, -0.634, -0.162]'),
    (4, '[-0.710, 0.330, 0.656, 0.041, -0.990, 0.726, 0.385, -0.958]');


-- KNN style query
select
  rowid,
  distance
from vec_examples
where sample_embedding match '[0.890, 0.544, 0.825, 0.961, 0.358, 0.0196, 0.521, 0.175]'
order by distance
limit 2;
/*
┌───────┬──────────────────┐
│ rowid │     distance     │
├───────┼──────────────────┤
│ 2     │ 2.38687372207642 │
│ 1     │ 2.38978505134583 │
└───────┴──────────────────┘
*/
```

Now we can just take the vectors we created earlier and store them in a table which can update as content changes.

```
CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  description TEXT.
  embeddings TEXT
);

CREATE VIRTUAL TABLE vec_posts USING vec0(
  id INTEGER PRIMARY KEY,
  embedding float[768]
);

-- Sync vectors
INSERT INTO vec_posts(id, embedding) SELECT id, embeddings FROM posts;
```

> We could also setup triggers to keep them up to date but in PocketBase I am using event hooks to keep the virtual table udpated.

## Generate the Recommendation

Now to generate the recommendation offline we just need to use one of the blog posts to use as the input query to then use [k-nearest neighbor search (kNN)](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html) to get N number of related posts.

```
SELECT
  vec_posts.id as id,
  vec_posts.embedding as embedding,
  posts.title as title,
  posts.description as description,
  posts.slug as slug
FROM vec_posts
INNER JOIN vec_posts.id = posts.id
WHERE embedding match ?
AND k = 6
ORDER BY distance;
```

We just need to provide the ? argument with the vector of the currently selected blog post, and then after we filter out the current blog post from the list then we have the N closest number of blog posts that are related in a vector database.

## Conclusion

This makes it so no matter how many times a blog posts is visited no network calls are made for the recommendation which enables this to scale really well.

To see this in action you can click around on the various blog posts I have on my site and see the generated descriptions and related posts at the end of each article.