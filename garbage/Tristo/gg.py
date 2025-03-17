
d = {}

d['a'] = 1
d['b'] = 2
d['z'] = 3
d['c'] = 3

df= {'e':4,'g':3}
new_d = d | df
print(new_d)
my_dict = {'a': 1, 'b': 2, 'c': 3}

# Pop the first item (this is based on insertion order, so it works on Python 3.7+)
first_key, first_value = next(iter(my_dict.items()))  # Get the first item
print(f"First item: {first_key}: {first_value}")

# Remove the first item
my_dict.pop(first_key)
print(f"Dictionary after pop: {my_dict}")
my_dict = {'a': 1, 'b': 2, 'c': 3}

# Reverse the order of the dictionary
reversed_dict = dict(reversed(list(my_dict.items())))
print(reversed_dict)

print(len(reversed_dict))
