import json

from panoramix.utils.helpers import C

def getAbiJson(data=None):

    if data == None:
        print('No data present')
        return

    """

        Please note:
        - function parameter names may be off
        - tuple parameters are not handled properly

    """

    res = []

    problems = []

    funcs = data['functions']

    for fname in data['problems']:
        funcs.append({
                'name': fname,
                'hash': '0x00000000',
            })

    for f in funcs:

#        'const' -> pure
#        'nonpayable' -> nonpayable
#        'payable' -> payable

        name = f['name']
        if 'unknown' in name and '?' in name:
            problems.append(f['hash'])
            continue

        name, params = name.split('(')
        params = params[:-1].split(', ')

        if '0x' not in f['hash']:
            assert f['name'] == '_fallback()'

            func = {
                'type': 'fallback',
            }

        else:

            func = {
                'type': 'function',
                'name': name,
                'inputs': []
            }


        if 'const' in f and f['const']:
            func['stateMutability'] = 'pure'

        # todo: handle stateMutability: 'view'

        elif 'payable' in f and f['payable']:
            func['stateMutability'] = 'payable'

        elif 'hash' != '0x00000000':
            func['stateMutability'] = 'nonpayable'

        for p in params:
            if p == '': 
                continue

            if ' ' not in p:
                func['inputs'].append(p)
            else:
                ptype, pname = p.split(' ')
                pname = pname[1:] # remove leading '_'

                func['inputs'].append({
                        'name': pname,
                        'type': ptype})

        res.append(func)


    if len(problems) > 0:
        print('Functions not included')
        for p in problems:
            print('- ' + p)
        print('(no signatures found)')
        print()

    return res
