import requests

# With this script you can make an API call to the Twitter API to retrieve the number of tweets of a specific program
# The library requests needs to be installed to make a http request.
# In this example a predefined list is used of PIDS

pids_list = ['b00plj0l', 'b00vlq0y', 'b03w65tp', 'b03w65x6', 'b03w65x8', 'b03wwx6z', 'b03xh92k', 'b03xh92m', 'b03xg9yn', 'b03xpvml', 'b03wctdg', 'b03wwxdb', 'b03wwxfk', 'b03t8r4h', 'b03vlf47', 'b03xg92x', 'b03wwxhr', 'b03wwxjr', 'b03wwxkl', 'b03wwxl9', 'b03wwxlc', 'b03yb36s']
len_pids_list = len(pids_list)

for i in range(0, len_pids_list):
    api_url = 'http://urls.api.twitter.com/1/urls/count.json?url=http://www.bbc.co.uk/programmes/'+pids_list[i]+'&callback=twttr.receiveCount'
    r = requests.get(api_url)
    result = r.text
    print("pid: ", pids_list[i], "have: ", result)