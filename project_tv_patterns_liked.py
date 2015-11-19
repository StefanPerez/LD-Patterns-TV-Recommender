import csv
import requests

# get_user_out_of_csv -> checking for each user which programs he or she watched and which programs not.
# The values are stored into two variables: liked_programs and disliked_programs
# The values are passed to the next function: get_viewing_time
def get_user_out_of_csv(user):
    liked_programs = []
    disliked_programs = []
    with open('source/to/file.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        csv_headings = next(csv_reader)
        print(csv_headings)
        for row in csv_reader:
            if row[2] == user:
                if row[4] == '0':
                    disliked_programs.append(row)
                else:                    
                    liked_programs.append(row)
    get_viewing_time(liked_programs,disliked_programs)


# get_viewing_time -> find the specific session of each liked and disliked programs and stored them in variable to passed them to the next function	
def get_viewing_time(liked, disliked):    
    length_liked_list = len(liked)
    length_disliked_list = len(disliked)

    sessions_id_of_liked_programs = []
    sessions_id_of_disliked_programs = []
    for i in range(0, length_liked_list):
        sessions_id_of_liked_programs.append(liked[i][0])

    for i in range(0, length_disliked_list):
        sessions_id_of_disliked_programs.append(disliked[i][0])

    get_pids_by_session_id(sessions_id_of_liked_programs,sessions_id_of_disliked_programs)


# Based on the session id that is passed from the function get_viewing_time a call to the session_activities table is done via csv.
def get_pids_by_session_id(liked_programs, disliked_programs):    
    len_liked = len(liked_programs)
    pids_of_liked_programs = []
    with open('source/to/file.csv') as f:
            csv_reader = csv.reader(f, delimiter=',')
            csv_headings = next(csv_reader)
            print(csv_headings)
            for row in csv_reader:
                for i in range(0, len_liked):
                    if row[0] == liked_programs[i]:
                        pids_of_liked_programs.append(row[1])

    get_twitter_score(pids_of_liked_programs)
    call_api(pids_of_liked_programs)


# Only the liked programs are passed to the get_twitter_score function. For each program an API call is been made to the TWITTER API
# The number of tweets are returned based on the pids.
def get_twitter_score(pids):
    len_pids_list = len(pids)
    twitter_pid_count = []
    for i in range(0, len_pids_list):
        api_url = 'http://urls.api.twitter.com/1/urls/count.json?url=http://www.bbc.co.uk/programmes/'+pids[i]
        r = requests.get(api_url)
        result = r.json()
        twitter_count = result['count']
        twitter_pid_count.append(twitter_count)
        stored_twitter_results.append([pids[i], result])
    print("popularity on twitter: ", twitter_pid_count)
    calculate_average_twitter_count_value(twitter_pid_count)

# Calculating all the parameters that is used within the weighted rating algorithm
# The values are passed to the weighted_rating function
def calculate_average_twitter_count_value(twitter_results):
    total = sum(twitter_results)
    total_average = total / len(twitter_results)
    patterns = [2, 2, 2, 2,2, 2, 2, 2,2, 2, 2, 2,4]
    for i in range(0, len(twitter_results)):
        single_result = twitter_results[i]
        number_of_patterns = patterns[i]
        weighted_rating(single_result,total_average, number_of_patterns)


# The weighted rating is calculated per program and is been stored in a variable
def weighted_rating(message_count, twit_average, numpatterns):
    if(numpatterns <= 5):
        value = 1
    else:
        value = 5
    R = message_count       # Popularity score of the TV program on Twitter = (Rating)
    p = numpatterns         # number of patterns between two programs = (Patterns)
    m = value               # minimum patterns needed to be listed in the Top 10
    C = twit_average        # the mean popularity score across all the TV programs

    WR = (p * R + m * C)/(p + m)
    stored_value.append(WR)
    call_api(WR)


def call_api(getpid,WR):
    for i in range(len(getpid) - 1):
        for j in range(i+1, len(getpid)):
            api_url = 'http://vistatv.eculture.labs.vu.nl//get_patterns_between_programmes?pid='+getpid[i]+'&pid='+getpid[j]+'&indent=true'
            r = requests.get(api_url)
            json_data = r.json()
            number_of_patterns = len(json_data)
            r = requests.get('http://www.bbc.co.uk/programmes/'+getpid[i]+'.json')
            json_data = r.json()
            output_json = str(json_data["programme"]["display_title"]["title"])
            ranking = [number_of_patterns,getpid[i], output_json,WR]
            ranking_pid.append(ranking[:])
        sort_patterns(ranking_pid)


def sort_patterns(rankings):
    # Sort the output based on # of patterns
    sorted_ranking_pid = sorted(rankings, reverse=True)
    if len(sorted_ranking_pid)>10:
        sorted_ranking_pid = sorted_ranking_pid[:10]
    # If results are less than 5, search through patterns from other recommendations
    max_results = 10
    length_of_ranking_pid = len(rankings)
    
    if length_of_ranking_pid < max_results:
        get_first_element_or_ranking = sorted_ranking_pid[0]
        get_first_pid_of_ranked_list = get_first_element_or_ranking[1]
        call_api(get_first_pid_of_ranked_list)
    else:
        stored_value.append(sorted_ranking_pid)


def run_project():
    with open('source/to/file/of/users.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if (row[1] >= '2014-03-01 00:00:00') and (row[1] <= '2014-03-31 23:59:59'):
                get_user_out_of_csv(row[2])



ranking_pid = []	
stored_value = []
stored_twitter_results = []
run_project()



