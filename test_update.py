import itertools
import pytest
import main

def test_update():
    config = {
        'ginger': {
            'django': 2,
            'flask': 3,
        },
        'cucumber': {
            'flask': 1,
        },
    }

    main.update(config, 'pylons', 7)
    # Пришлось немного изменить тест, ведь при таких
    #  исходных данных оба результата одинаково
    #  удовлетворяют условию
    res = [{
        'ginger': {
            'django': 2,
            'flask': 3,
            'pylons': 1,
        },
        'cucumber': {
            'flask': 1,
            'pylons': 6,
        },
    },
        {
            'ginger': {
                'django': 2,
                'flask': 3,
                'pylons': 2,
            },
            'cucumber': {
                'flask': 1,
                'pylons': 5,
            },
        }
    ]
    assert config in res

@pytest.mark.parametrize('name, amount, expected', [
    ('flask', 15, {'huston': 15, 'miami': 15, 'orlando': 15}),
    ('pyramid', 2, {'huston': 10, 'miami': 11, 'orlando': 11})
])
def test_update_param(name, amount, expected):
    config = {
        'huston': {
            'django': 5,
            'flask': 3,
        },
        'miami': {
            'flask': 11,
        },
        'orlando': {
            'flask': 11,
        },
    }

    main.update(config, name, amount)
    print(config)
    assert {k: sum(v.values()) for k, v in config.items()} == expected

def test_initial():
    config = {
        'ginger': {},
        'cucumber': {},
    }

    main.update(config, 'flask', 3)
    main.update(config, 'django', 3)

    assert sum(config['ginger'].values()) == sum(config['cucumber'].values())
    assert sum(sum(x.values()) for x in config.values()) == 3+3


# @pytest.mark.xfail(reason="Advanced test. Optional to implement")
def test_predictable_config():
    permutations = []
    services = [
        ('flask', 7),
        ('django', 13),
        ('pylons', 17)
    ]

    for permutation in itertools.permutations(services):
        config = {
            'ginger': {},
            'cucumber': {},
        }
        for svc, num in permutation:
            main.update_with_predicted_config(config, svc, num)
        assert sum(sum(x.values()) for x in config.values()) == 7+13+17
        permutations.append(config)

    assert all(p == permutations[0] for p in permutations[1:])