"""
字典操作
"""


def get_info(name, data):
    _info = {}
    for k, v in data.items():
        try:
            if isinstance(v, dict):
                v = v[name]
            _info[k] = v
        except KeyError:
            return None
    return _info
    

def main():
    info_dict = {
        'Dept': {'Tom': 'Marketing Dept', 'Amy': 'Web Develop Dept', 'Cindy': 'HR Dept'},
        'Age': {'Tom': 30, 'Amy':25, 'Cindy': 25},
        'Diploma': {'Tom': 'master', 'Amy': 'dpctor', 'Cindy': 'bachelor '}
    }
    print(get_info('Amy', info_dict))


if __name__ == '__main__':
    main()