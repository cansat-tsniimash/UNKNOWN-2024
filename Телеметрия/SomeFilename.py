import csv
from pprint import pprint

def load_csv(file_path: str, strip_headers=True):
	lines = []

	with open(file_path, mode="r") as stream:
		if strip_headers:
			stream.readline()

		while True:
			line = stream.readline()
			if not line:
				break

			line = line.strip()
			parts = line.split(";")
			lines.append(parts)
		
	return lines


def get_nearest(lines, score_finder):
	min_score = None
	rv_line = None
	for line in lines:
		line_score = score_finder(line)
		if min_score is None or min_score > line_score:
			rv_line = line
			min_score = line_score

	return rv_line 



packet2_lines = load_csv("./тест2/packet2.csv")
packet3_lines = load_csv("./тест2/packet3.csv")
GoodFile = open("./File.csv", "w")


for p3_line in packet3_lines:
	p3_time = int(p3_line[1])

	def score(line):
		p2_time = int(line[1])
		return abs(p2_time - p3_time)

	matching_p2_line = get_nearest(packet2_lines, score)
	
	GoodFile.write(p3_line[4]+",")
	GoodFile.write(p3_line[3]+",")
	GoodFile.write(matching_p2_line[5])
	GoodFile.write('\n')
	GoodFile.flush()
	print(p3_line, matching_p2_line)

