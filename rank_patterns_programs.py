import csv
import requests
import pprint

def init_pid(programme):
    #print("pid used: ", programme)
    pid = programme
    print("pid used:", pid)
    key = 'http://www.bbc.co.uk/programmes/'+pid+'#programme'
    result = []
    with open('source/to/pattern/file.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            if row[0].strip() == key:
                result.append(row[1].strip())
                print("pids in csv:", row[1].strip())

    pid_program = []

    for i in range(len(result)):
        string_result = result[i]
        l2s_result = str(string_result)
        test = l2s_result[32:-10]
        pid_program.append(test)

    print(pid,pid_program)
    #call_api(pid, pid_program)
    return

def call_api(getpid, get_program):

    for i in range(len(get_program)):
        api_url = 'http://vistatv.eculture.labs.vu.nl//get_patterns_between_programmes?pid='+getpid+'&pid='+get_program[i]+'&indent=true'
        r = requests.get(api_url)
        json_data = r.json()
        number_of_patterns = len(json_data)
        r = requests.get('http://www.bbc.co.uk/programmes/'+get_program[i]+'.json')
        json_data = r.json()
        output_json = str(json_data["programme"]["display_title"]["title"])
        ranking = [number_of_patterns,get_program[i], output_json]
        ranking_pid.append(ranking[:])
    sort_patterns(ranking_pid)
    return


def sort_patterns(rankings):
    # Sort the output based on # of patterns
    sorted_ranking_pid = sorted(rankings, reverse=True)
    if len(sorted_ranking_pid)>10:
        sorted_ranking_pid = sorted_ranking_pid[:10]
    # If results are less than 5, search through patterns other recommendations
    max_results = 10
    length_of_ranking_pid = len(rankings)

    #print("max resultaat: ",max_results, "length of the list: ",length_of_ranking_pid, "check: ", length_of_ranking_pid < max_results )
    if length_of_ranking_pid < max_results:
        get_first_element_or_ranking = sorted_ranking_pid[0]
        get_first_pid_of_ranked_list = get_first_element_or_ranking[1]
        init_pid(get_first_pid_of_ranked_list)
    else:
        #print("recommended",len(sorted_ranking_pid),"results,based on # of patterns:",sorted_ranking_pid)
        print("recommended",len(sorted_ranking_pid),"results,based on # of patterns:",sorted_ranking_pid)
    return

ranking_pid = []
print(init_pid('b020svhc'))

### PRINT ALL THE RESULTS
#print("Patterns with no ranking \n", list(enumerate(ranking_pid, start=1)), " \n")
#print("Patterns with # of patterns ranking \n", list(enumerate(sorted_ranking_pid, start=1)), "\n")
#print(number_of_patterns, "patterns between pid: ", pid_program[i])


