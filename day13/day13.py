from copy import deepcopy

def fold_across_horizontal_line(coords, y_pos):
    translated_coords = []
    for c in coords:
        if c[0] > y_pos:
            # needs folding
            new_y_pos = y_pos - (c[0]-y_pos)
            translated_coords.append((new_y_pos, c[1]))
        else:
            translated_coords.append((c[0],c[1]))

    return list(set(translated_coords))

def fold_across_vertical_line(coords, x_pos):
    translated_coords = []
    for c in coords:
        if c[1] > x_pos:
            # needs folding
            new_x_pos = x_pos - (c[1]-x_pos)
            translated_coords.append((c[0],new_x_pos))
        else:
            translated_coords.append((c[0],c[1]))

    return list(set(translated_coords))

def fold_across_line(coords, fold):
    # fold is in format 'fold along y=7'
    direction = fold[11:12]
    line_pos = int(fold[13:])

    if direction == 'x':
        return fold_across_horizontal_line(coords, line_pos)
    else:
        return fold_across_vertical_line(coords, line_pos)

def plot_coords(coords):
    max_x = 0
    max_y = 0
    for c in coords:
        max_x = max(max_x, c[0])
        max_y = max(max_y, c[1])

    plotted = []
    for i in range(max_y+1):
        row = ['.'] * (max_x+1)
        plotted.append(row)

    for c in coords:
        plotted[c[1]][c[0]] = '#'

    return plotted

def main():
    with open('input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    # coords are x,y
    coords = []
    folds = []
    for l in lines:
        if len(l.strip()) == 0:
            continue
        elif 'fold' in l:
            folds.append(l.strip())
        else:
            coord = [int(x) for x in l.strip().split(',')]
            coords.append((coord[0], coord[1]))

    print(coords)
    print(folds)

    for f in folds:
        coords = fold_across_line(coords, f)

    plotted = plot_coords(coords)
    for p in plotted:
        print(p)

if __name__ == "__main__":
	main()
