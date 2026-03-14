---
name: twitter
version: 1.0.0
description: Twitter/X data lookup — search tweets, user profiles, followers, replies. Use when the user asks about Twitter activity, social signals, or wants to look up accounts.
tools:
  - twitter_search_tweets
  - twitter_get_tweets
  - twitter_user_info
  - twitter_user_tweets
  - twitter_user_followers
  - twitter_user_followings
  - twitter_tweet_replies
  - twitter_tweet_retweeters
  - twitter_search_users

metadata:
  starchild:
    emoji: "🐦"
    skillKey: twitter
    requires:
      env: [TWITTER_API_KEY]

user-invocable: false
disable-model-invocation: false
---

# Twitter / X Data

Read-only access to Twitter/X via twitterapi.io. Use these tools to look up tweets, users, followers, and social activity.

## Tool Decision Tree

**"Search for tweets about a topic"** → `twitter_search_tweets`
Advanced query with operators: keywords, from:user, #hashtag, $cashtag, min_faves, date ranges.

**"Look up a specific tweet or set of tweets"** → `twitter_get_tweets`
Pass one or more tweet IDs directly.

**"Who is this Twitter account?"** → `twitter_user_info`
Profile data: bio, follower count, tweet count, verification.

**"What has this account been posting?"** → `twitter_user_tweets`
Recent tweets from a specific user.

**"Who follows this account?"** → `twitter_user_followers`
List of followers for a user.

**"Who does this account follow?"** → `twitter_user_followings`
List of accounts a user follows.

**"What are people saying in reply to this tweet?"** → `twitter_tweet_replies`
Replies to a specific tweet by ID.

**"Who retweeted this?"** → `twitter_tweet_retweeters`
Users who retweeted a specific tweet.

**"Find accounts related to a topic"** → `twitter_search_users`
Search users by name or keyword.

## Available Tools

| Tool | Description | Key Params |
|------|-------------|------------|
| `twitter_search_tweets` | Advanced tweet search | `query` (required), `cursor` |
| `twitter_get_tweets` | Get tweets by ID | `tweet_ids` (array, required) |
| `twitter_user_info` | User profile lookup | `username` (required) |
| `twitter_user_tweets` | User's recent tweets | `username` (required), `cursor` |
| `twitter_user_followers` | User's followers | `username` (required), `cursor` |
| `twitter_user_followings` | User's followings | `username` (required), `cursor` |
| `twitter_tweet_replies` | Replies to a tweet | `tweet_id` (required), `cursor` |
| `twitter_tweet_retweeters` | Who retweeted | `tweet_id` (required), `cursor` |
| `twitter_search_users` | Search for users | `query` (required), `cursor` |

## Usage Patterns

### Research an account
1. `twitter_user_info` — get profile, follower count, bio
2. `twitter_user_tweets` — see what they've been posting
3. `twitter_user_followings` — who they follow (reveals interests)

### Track a topic or token
1. `twitter_search_tweets` with query like `"$SOL min_faves:50"` — find popular tweets
2. `twitter_search_users` with the topic — find relevant accounts
3. Follow up with `twitter_user_info` on interesting accounts

### Analyze engagement on a tweet
1. `twitter_get_tweets` — get the tweet and its metrics
2. `twitter_tweet_replies` — see the conversation
3. `twitter_tweet_retweeters` — see who amplified it

### Find influencers in a space
1. `twitter_search_users` with keyword (e.g. "DeFi analyst")
2. `twitter_user_info` on top results to compare follower counts
3. `twitter_user_tweets` to check content quality

## Search Query Operators

The `twitter_search_tweets` tool supports advanced operators:

| Operator | Example | Description |
|----------|---------|-------------|
| keyword | `bitcoin` | Tweets containing the word |
| exact phrase | `"ethereum merge"` | Exact phrase match |
| `from:` | `from:elonmusk` | Tweets by a specific user |
| `to:` | `to:elonmusk` | Tweets replying to a user |
| `#hashtag` | `#crypto` | Tweets with hashtag |
| `$cashtag` | `$BTC` | Tweets with cashtag |
| `lang:` | `lang:en` | Filter by language |
| `has:media` | `has:media` | Tweets with images/video |
| `has:links` | `has:links` | Tweets with URLs |
| `is:reply` | `is:reply` | Only replies |
| `min_faves:` | `min_faves:100` | Minimum likes |
| `min_retweets:` | `min_retweets:50` | Minimum retweets |
| `since:` | `since:2024-01-01` | Tweets after date |
| `until:` | `until:2024-12-31` | Tweets before date |

Combine operators: `from:VitalikButerin $ETH min_faves:100 since:2024-01-01`

## Pagination

Most endpoints support cursor-based pagination. When a response includes a cursor value, pass it as the `cursor` parameter to get the next page. If no cursor is returned, you've reached the end.

## Notes

- **API key required**: Set `TWITTER_API_KEY` environment variable. Tools will error without it.
- **Read-only**: These tools only retrieve data. No posting, liking, or following.
- **Usernames**: Always pass without the `@` prefix (e.g. `"elonmusk"` not `"@elonmusk"`).
- **Tweet IDs**: Use string format for tweet IDs to avoid integer overflow issues.
- **Rate limits**: The API has rate limits. If you get rate-limited, wait before retrying.
