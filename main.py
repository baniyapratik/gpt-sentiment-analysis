import openai
import praw

openai.api_key = '<openai-api-key>'
client_id = '<reddit-client-id>'
client_secret = '<reddit-client-secret>'
reddit = praw.Reddit(client_id=client_id,
                    client_secret=client_secret, user_agent="sentiment analysis test")

def get_titles_and_comments(subreddit="stocks", sub_instance="hot", limit=5, num_comments=2, skip_first=2):
    subreddit = reddit.subreddit(subreddit)
    titles_and_comments = {}
    for c, post in enumerate(getattr(subreddit, sub_instance)(limit=limit)):
        
        if c < skip_first:
            continue
        
        c+=(1-skip_first)
        
        titles_and_comments[c] = ""

        submission = reddit.submission(post.id)
        title = post.title
        
        titles_and_comments[c] += "Title: " + title  + "\n\n"
        titles_and_comments[c] += "Comments: \n\n"
        
        comment_counter = 0
        for comment in submission.comments:
            comment = comment.body
            if not comment == "[deleted]":
                titles_and_comments[c] += comment + "\n"
                comment_counter+=1
            if comment_counter == num_comments:
                break

    return titles_and_comments


def create_prompt(title_and_comments):
    task = """Return the stock ticker or company name mentioned in the following title and comments and classify the sentiment around the company as positive, negative or neutral. 
            If no ticker or company is mentioned write 'No company mentioned' \n\n"""
    return  task +  title_and_comments

if __name__ == "__main__":
    print("Get titles and comments...")
    titles_and_comments = get_titles_and_comments()

    for key, title_with_comments in titles_and_comments.items():
        prompt = create_prompt(title_with_comments)

        response = openai.Completion.create(engine="text-davinci-003",
                                                prompt=prompt,
                                                max_tokens=256,
                                                temperature=0,
                                                top_p=1.0,
                                                frequency_penalty=0.0,
                                                presence_penalty=0.0)

        print("Sentiment: " + response["choices"][0]["text"])
        print("-"*30)
