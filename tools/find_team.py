

def find_team(source):
    target = {}
    for s in source:
        if s['belong_to'] is None:
            if s['name'] not in target:
                t_dict = {'name': s['name'], 'team': []}
                target[s['name']] = t_dict
        else:
            if s['belong_to'] in target:
                target[s['belong_to']]['team'].append({'name': s['name']})
            else:
                t_dict = {'name': s['belong_to'], 'team': [{'name': s['name']}]}
                target[s['belong_to']] = t_dict

    return target.values()



if __name__ == '__main__':
    # 源数据
    s = [{'name': 'leader-1', 'belong_to': None}, {'name': 'jack', 'belong_to': 'leader-2'},
         {'name': 'lili', 'belong_to': 'leader-1'}, {'name': 'leader-2', 'belong_to': None},
         {'name': 'Tom', 'belong_to': 'leader-1'}]
    # 目标数据
    # d = [
    #     {'name': 'leader-1', 'team': [{'name': 'lili'}, {'name': 'Tom'}]},
    #     {'name': 'leader-2', 'team': [{'name': 'jack'}]}
    # ]
    d = list(find_team(s))
    print(d)



