testdata0 = {
    "game": {
        "id": "",
        "ruleset": {
            "name": "standard",
            "version": "cli",
            "settings": {
                "foodSpawnChance": 15,
                "minimumFood": 1,
                "hazardDamagePerTurn": 14,
                "hazardMap": "",
                "hazardMapAuthor": "",
                "royale": {
                    "shrinkEveryNTurns": 25
                },
                "squad": {
                    "allowBodyCollisions": True,
                    "sharedElimination": True,
                    "sharedHealth": True,
                    "sharedLength": True
                }
            }
        },
        "timeout": 500,
        "source": ""
    },
    "turn": 0,
    "board": {
        "height": 11,
        "width": 11,
        "snakes": [
            {
                "id": "one",
                "name": "ONE",
                "latency": "0",
                "health": 0,
                "body": [
                    {
                        "x": 3,
                        "y": 3
                    }
                ],
                "head": {
                    "x": 3,
                    "y": 3
                },
                "length": 1,
                "shout": "",
                "squad": "",
                "customizations": {
                    "color": "#123456",
                    "head": "safe",
                    "tail": "curled"
                }
            },
            {
                "id": "two",
                "name": "TWO",
                "latency": "0",
                "health": 0,
                "body": [
                    {
                        "x": 4,
                        "y": 3
                    }
                ],
                "head": {
                    "x": 4,
                    "y": 3
                },
                "length": 1,
                "shout": "",
                "squad": "",
                "customizations": {
                    "color": "#654321",
                    "head": "silly",
                    "tail": "bolt"
                }
            }
        ],
        "food": [],
        "hazards": []
    },
    "you": {
        "id": "one",
        "name": "ONE",
        "latency": "0",
        "health": 0,
        "body": [
            {
                "x": 3,
                "y": 3
            }
        ],
        "head": {
            "x": 3,
            "y": 3
        },
        "length": 1,
        "shout": "",
        "squad": "",
        "customizations": {
            "color": "#123456",
            "head": "safe",
            "tail": "curled"
        }
    }
}


testdata1 = {
    'game':
    {
        'id': 'faffa4d9-6cf2-423d-854e-214c094f5d24',
        'ruleset':
        {
            'name': 'wrapped',
            'version': 'v1.0.25',
            'settings':
            {
                'foodSpawnChance': 15,
                'minimumFood': 1,
                'hazardDamagePerTurn': 14,
                'royale':
                {
                    'shrinkEveryNTurns': 0
                },
                'squad':
                {
                    'allowBodyCollisions': False,
                    'sharedElimination': False,
                    'sharedHealth': False,
                    'sharedLength': False
                }
            }
        },
        'timeout': 500,
        'source': 'custom'
    },
    'turn': 0,
    'board':
    {
        'height': 11,
        'width': 11,
        'snakes': [
            {
                'id': 'gs_R49k9PH4pk7SMGCCfvHxSD9P',
                'name': 'ClumsyTestsnake',
                'latency': '',
                'health': 100,
                'body': [
                    {'x': 1, 'y': 1}, {'x': 1, 'y': 1}, {'x': 1, 'y': 1}
                ],
                'head': {'x': 1, 'y': 1},
                'length': 3,
                'shout': '',
                'squad': '',
                'customizations':
                {'color': '#ff00ff', 'head': 'default', 'tail': 'default'}
            },
            {
                'id': 'gs_mctWCVDVRJK38yDPDM4m7Qwd',
                'name': 'SnakeInABank',
                'latency': '',
                'health': 100,
                'body': [
                    {'x': 9, 'y': 1}, {'x': 9, 'y': 1}, {'x': 9, 'y': 1}
                ],
                    'head': {'x': 9, 'y': 1},
                    'length': 3,
                    'shout': '',
                    'squad': '',
                    'customizations':
                    {'color': '#736ccb', 'head': 'default', 'tail': 'curled'}
            }
        ],
        'food': [{'x': 2, 'y': 0}, {'x': 10, 'y': 2}, {'x': 5, 'y': 5}],
        'hazards': []
    },
    'you':
    {
        'id': 'gs_R49k9PH4pk7SMGCCfvHxSD9P',
        'name': 'ClumsyTestsnake',
        'latency': '',
        'health': 100,
        'body': [
            {'x': 1, 'y': 1}, {'x': 1, 'y': 1}, {'x': 1, 'y': 1}
        ],
            'head': {'x': 1, 'y': 1},
            'length': 3,
            'shout': '',
            'squad': '',
            'customizations': {'color': '#ff00ff', 'head': 'default', 'tail': 'default'}
    }
}
