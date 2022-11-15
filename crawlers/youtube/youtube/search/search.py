class Search:

    def __init__(self, video_id, title: str, url: str, comments, videos, token):
        self.video_id = video_id
        self.title = title
        self.url = url
        self.comments = comments
        self.videos = videos
        self.token = ''

    def get_comments(youtube, self):
        try:
            video_response = youtube.commentThreads().list(part='snippet',
                                               videoId=self.video_id,
                                               pageToken=self.token).execute()
            for item in video_response['items']:
                comment = item['snippet']['topLevelComment']
                text = comment['snippet']['textDisplay']
                self.comments.append(text)
            if "nextPageToken" in video_response:
                return Search.get_comments(youtube, self.video_id, self.comments, video_response['nextPageToken'])
            else:
                return self.comments
        except Exception:
            return 'Comments Disabled'

    def video(keyword, youtube):
        videos = []
        request = youtube.search().list(q=keyword, part='snippet', maxResults=10, type='video')
        res = request.execute()
        for item in res['items']:
            video = {
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'url': 'https://www.youtube.com/watch?v=' + (item['id']['videoId']),
                'comments': Search.get_comments(youtube, item['id']['videoId'])
            }
            videos.append(video)
        return videos
