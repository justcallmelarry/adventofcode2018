import os
import sys


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = []

    def load_input(self):
        if any([x in sys.argv for x in ('--test', '-t')]):
            self.input = os.path.join(self.filepath, 'sample.txt')
        if any([x in sys.argv for x in ('--all', '-a')]):
            self.input = os.path.join(self.filepath, 'all_samples.txt')
        with open(self.input, 'r') as input_file:
            for line in input_file.read().split('\n'):
                if line == '':
                    continue
                line = line.split(' ')
                self.input_list.append([int(line[0]), int(line[-2])])

    def output(self, *_output):
        self._results += [str(x) for x in _output]

    def results(self):
        output = '\n'.join(self._results)
        print(output)
        with open(os.path.join(self.filepath, 'results.txt'), 'w') as results_file:
            results_file.write(output)

    def run(self):
        def get_relative_pos(marble, circle_size, steps, clockwise):  # 1 + 2
            if clockwise:
                pos = marble + steps  # 3
            else:
                pos = marble - steps
                if pos < 0:
                    pos = circle_size + pos + 1
            while pos > circle_size:  # 3 > 1
                pos -= circle_size + 1
            return pos

        for game_id, game in enumerate(self.input_list):
            players = game[0]
            score = {}
            circle = [0]
            current_marble_pos = 0
            current_player = 1
            for marble in range(1, game[1] * 100 + 1):
                circle_size = len(circle)
                if circle_size == 1:
                    circle.append(marble)
                    current_marble_pos = 1
                elif marble % 23 == 0:
                    if current_player not in score:
                        score[current_player] = 0
                    score[current_player] += marble
                    current_marble_pos = get_relative_pos(current_marble_pos, circle_size - 1, 7, False)
                    extra = circle.pop(current_marble_pos)
                    score[current_player] += extra
                else:
                    current_marble_pos = get_relative_pos(current_marble_pos, circle_size - 1, 2, True)
                    if current_marble_pos == 0:
                        circle.append(marble)
                        current_marble_pos = -1
                    else:
                        circle.insert(current_marble_pos, marble)
                if current_player == players:
                    current_player = 1
                else:
                    current_player += 1

            winning_player = max(score, key=score.get)
            self.output(f'winner: elf #{winning_player}', f'winning score: {score.get(winning_player)}', ' ')


if __name__ == "__main__":
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()