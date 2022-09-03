MOVIES = {
	'jaws': {'showtimes': [12.33, 15.5, 18.5, 21.5], 'runtime':2.15, 'priority':10},
	'cobra': {'showtimes': [9.5, 13.66, 17.75, 21.75], 'runtime': 3, 'priority':9},
	'bullet_train': {'showtimes': [9.66, 13.33, 17.0, 20.33], 'runtime': 2.1, 'priority': 9},
	'nope': {'showtimes': [10.66, 17.33, 21.0], 'runtime': 2.25, 'priority': 10},
	'breaking': {'showtimes': [16, 22], 'runtime': 1.75, 'priority': 3},
	'ttyol': {'showtimes': [11, 14, 17, 19.75, 22.66], 'runtime': 1.8, 'priority': 5},
	'blob': {'showtimes': [9.75, 14.5, 16.75, 19.33], 'runtime': 1.33, 'priority': 6}
}

def find_best_it(movies):
	solution = [[]]
	max_value = [0.0]
	dfs(movies, 0.0, [], 0.0, solution, max_value)
	print(solution[-1], max_value[-1])

def dfs(movies, time, cur, value, solution, max_value):
	if value > max_value[0]:
		solution[0] = cur
		max_value[0] = value
		# print(value, cur, solution, max_value)
	if len(cur) >= len(movies) or time > 24:
		return
	for m in movies:
		print(time, value, cur, m, max_value, solution)
		# input()
		new_start = time
		if m not in {c[0] for c in cur}:
			for t in movies[m]['showtimes']:
				if t > time:
					new_start = t
					dfs(movies, new_start + movies[m]['runtime'], cur + [(m, new_start)], value + movies[m]['priority'] * movies[m]['runtime'], solution, max_value)
					break


find_best_it(MOVIES)