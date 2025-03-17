class DecisionNode:
    def __init__(self, question, yes_action=None, no_action=None, priority=0):
        self.question = question
        self.yes_action = yes_action
        self.no_action = no_action
        self.priority = priority

    def decide(self, context):
        actions = []

        if self.question(context):
            if isinstance(self.yes_action, DecisionNode):
                actions.extend(self.yes_action.decide(context))
            else:
                if callable(self.yes_action):
                    actions.append((self.yes_action, self.priority))
        else:
            if isinstance(self.no_action, DecisionNode):
                actions.extend(self.no_action.decide(context))
            else:
                if callable(self.no_action):
                    actions.append((self.no_action, self.priority))

        actions.sort(key=lambda x: x[1], reverse=True)

        return [action[0](context) for action in actions]

# ---- Questions ----
def is_under_attack(context):
    return context['under_attack']

def resources_critical(context):
    return context['resources']['gold'] < 50 or context['resources']['food'] < 50

def buildings_insufficient(context):
    return not context['buildings'].get('storage', False)

def has_enough_military(context):
    return context['military_units'] >= 10


# ---- Actions ----
def defend(context):
    for unit in context['units']:
        if unit['type'] == 'military':
            unit['instance'].attack_entity(context['enemy_id'])
    return "Defending the village!"

def gather_resources(context):
    for unit in context['units']:
        if unit['type'] == 'villager' and not unit['instance'].is_full():
            unit['instance'].collect_entity(context['resource_id'])
    return "Gathering resources!"

def train_military(context):
    for building in context['buildings']['training']:
        building['instance'].train_unit(context['player'], context['current_time'], 'v')
    return "Training military units!"

def attack(context):
    for unit in context['units']:
        if unit['type'] == 'military':
            unit['instance'].attack_entity(context['enemy_id'])
    return "Attacking the enemy!"

def drop_resources(context):
    for unit in context['units']:
        if unit['type'] == 'villager' and unit['instance'].is_full():
            unit['instance'].drop_to_entity(context['drop_off_id'])
    return "Dropping off resources!"

# ---- Arbre de décision ----
tree = DecisionNode(
    is_under_attack,
    yes_action=DecisionNode(
        enemy_visible,
        yes_action=attack,
        no_action=defend,
        priority=10
    ),
    no_action=DecisionNode(
        resources_critical,
        yes_action=DecisionNode(
            buildings_insufficient,
            yes_action=gather_resources,
            no_action=drop_resources,
            priority=8
        ),
        no_action=DecisionNode(
            has_enough_military,
            yes_action=train_military,
            no_action=gather_resources,
            priority=7
        ),
        priority=9
    ),
    priority=10
)
