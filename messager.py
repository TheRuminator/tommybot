import praw, time,requests,json
print(f"Messager bot started at {time.ctime()}")
url = "https://api.npoint.io/c1905a42383b50a26a3f"
headers = {
  'Content-Type': 'application/json'
}  
def uploadUser(user:object):
    resp = requests.request("GET",url=url).json()
    resp['usersSentTo'] += f"{user.name} "
    data=json.dumps(resp)
    resp1 = requests.request("POST",url,headers=headers,data=data)

def downloadList():
    resp = requests.get(url).json()
    userList = resp['usersSentTo']
    return userList

resp1=requests.get(url).json()
message = resp1['message']


sub = "TheReservedBST"
reddit = praw.Reddit(client_id = "WVvTW6UOD243aeRZdPOmug",
                     client_secret = "SEPZtkOq1XVYPMEBH7BzM3Gjqo3qUw",
                     user_agent = "worker",
                     username = "VerifiedBot_",
                     password = "")


stream = reddit.subreddit(sub).stream.submissions(pause_after=-1,skip_existing=True)
comm_stream = reddit.subreddit(sub).stream.comments(pause_after=-1,skip_existing=True)

while True:
    for subm in stream:
        if subm is None:
            break
        try:
            li = downloadList()
            print(li)
            if subm.author.name not in li:
                subm.author.message(subject="TheReservedBST Newsletter",message=message,from_subreddit=sub)
                uploadUser(subm.author)
                print(f"Message sent to {subm.author}")
                time.sleep(1800)
        except Exception as e:
            print(f"error occured while sending message to {subm.author}\n{e}")
        
    for comm in comm_stream:
        if comm is None:
            break
        try:
            li = downloadList()
            print(li)
            if comm.author.name not in li:
                comm.author.message(subject="TheReservedBST Newsletter",message=message,from_subreddit=sub)
                uploadUser(comm.author)
                print(f"Message sent to {comm.author}")
                time.sleep(1800)
        except Exception as e:
            print(f"error occured while sending message to {comm.author}\n{e}")
