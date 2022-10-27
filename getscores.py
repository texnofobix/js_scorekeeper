import urllib.request
import json


def get_team_score(team_number):
    port = "3{}".format(str(team_number).rjust(3, '0')) # pad team number as 3XXX
    url = "http://localhost:{}/api/Challenges".format(port)

    score = {'Team': team_number, }

    try:
        with urllib.request.urlopen( url) as response:
            html = response.read()
            challenge_data = json.loads(html)
            possible_points  = 0
            earned_points = 0

            for challenge in challenge_data['data']:
                # disabledEnv Might need to ignore "Docker"

                if challenge['disabledEnv'] != 'Docker':
                    possible_points += challenge['difficulty']
                    # print(challenge['name'])
                    
                    if challenge['solved']:
                        score[challenge['name']] = True
                        earned_points += challenge['difficulty']
                    else:
                        score[challenge['name']] = False
            
            # return ('Team {}:'.format(team_number), earned_points, possible_points)
            #return {'Team': team_number}
            score['Earned'] = earned_points
            score['Possible'] = possible_points
            return score
            
    except urllib.error.URLError:
        #return ('Team {}:'.format(team_number), 'no response')
        return score
    

def get_all_team_scores(start,end):
    for team_number in range(1, end + 1):
        print(get_team_score(team_number))

get_all_team_scores(1,4)