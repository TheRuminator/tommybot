import praw, requests, json, time

print(f"Bot started at {time.ctime()}")

subredditt = 'TheReservedBST'

userFlairToSet = 'Verified Seller'
userFlairTemplateId = "851b0bc4-5e1f-11ed-9f09-0a0e35a5bac3"


userFlairAfterRemoved = '0 Transactions | New Trader'
userFlairAfterRemovedId = '4fc35366-d7b9-11eb-8d4a-0e93b66cc537'

postFlairToSet = 'VERIFIED SALE'

url = "https://api.npoint.io/c379aa784c6412e2206f"


payload = ""
headers = {
  'Content-Type': 'application/json'
}

trialVar1 = requests.get(url).json()
print(trialVar1)


def assignFlair(user):
    response = requests.get(url).json()
    usersAndDate = response['verifiedSellers'].split()
    users = []
    for useranddatestr in usersAndDate:
        users.append(useranddatestr.split(';')[0])
    if user in users:
        reddit.subreddit(subredditt).flair.set(user, text=userFlairToSet, flair_template_id = userFlairTemplateId)
        print(f'flair set for {user}')


def assignPostFlair(post):
    submission = reddit.submission(post.id)
    if submission.author_flair_text == userFlairToSet:
        choicers = post.flair.choices()
        for choice in choicers:
            if choice['flair_text'] == postFlairToSet:
                post.flair.select(choice['flair_template_id'])
        comm = submission.reply(body="Verified")
        comm.mod.distinguish(how="yes",sticky=True)
        print("Post flair assigned and comment made")


def removeUserFlair():
    response = requests.get(url).json()
    usersAndDate = response['verifiedSellers'].split()
    for users in usersAndDate:
        date = users.split(';')[1]
        dateutc = time.strptime(date,"%d-%m-%y")
        if time.gmtime()>dateutc:
            redditorStr = users.split(';')[0]
            redditor = reddit.redditor(redditorStr)
            reddit.subreddit(subredditt).flair.set(redditor, text=userFlairAfterRemoved, flair_template_id = userFlairAfterRemovedId)
            print(f'flair removed for {redditor}')
            usersAndDate.remove(users)
    stringT = " ".join(usersAndDate)
    data = {'verifiedSellers':stringT}
    datajson = json.dumps(data)
    headers = {
    'Content-Type': 'application/json'
    }
    resp = requests.request("POST",url,headers=headers,data=datajson)


while True:
    try:
        reddit = praw.Reddit(client_id = "FYcTa1vq5fSM4HDEKgwR9g",
                             client_secret = "pzkCd8fjVgLqGUP_DYekgC86yG8ghg",
                             user_agent = "worker",
                             username = "Reserved-Bot",
                             password = "")

        sub_stream = reddit.subreddit(subredditt).stream.submissions(pause_after=-1,skip_existing=True)
        comm_stream = reddit.subreddit(subredditt).stream.comments(pause_after=-1,skip_existing=True)

        while True:

            for comment in comm_stream:
                if comment is None:
                    break
                if comment.author_flair_text != userFlairToSet:
                    assignFlair(comment.author)
                removeUserFlair()
            for submission in sub_stream:
                if submission is None:
                    break
                if submission.author_flair_text != userFlairToSet:
                    assignFlair(submission.author)
                assignPostFlair(submission)
                removeUserFlair()

    except Exception as e:
        print("Error occured. Being handled and restarting bot",f"\n{e}\n--")
        time.sleep(20)
        print("Bot restarted")
        continue
