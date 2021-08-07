def read_file(file):
	i = 1
	ans_string = ""
	final_list = []
	with open(file, 'r') as f:
		# print(f.readlines())
		for line in f.readlines():
			ans_string = ans_string + line[:-1] + ','
			if i % 3 == 0:
				final_list.append(ans_string)
				ans_string = ""
			i += 1
	return final_list

data = read_file("trading_results.txt")

with open("trading_results1.txt", "w+") as f:
	for line in data:
		f.write(line + '\n')




