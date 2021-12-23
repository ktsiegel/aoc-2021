from copy import deepcopy

def print_image(im):
    for r in im:
        print(''.join(r))
    print(' ')

def get_enhanced_pixel(image, algo, row, col):
    pixel_code = ''
    for pix_row in range(max(0,row-1), min(len(image),row+2)):
        for pix_col in range(max(0,col-1), min(len(image[0]),col+2)):
            if image[pix_row][pix_col] == '.':
                pixel_code += '0'
            else:
                pixel_code += '1'
    pixel_index = int(pixel_code, 2)
    return algo[pixel_index]

def enhance_image(image, algo):
    output_image = []
    for row in range(len(image)):
        output_row = []
        for col in range(len(image[0])):
            output_row.append(get_enhanced_pixel(image, algo, row, col))
        output_image.append(output_row)
    return output_image

def add_border(im, width):
    im_out = []
    def append_vertical_buffer():
        for i in range(0,width):
            row_len = len(im[0]) + width*2
            row = ['.'] * row_len
            im_out.append(row)
    append_vertical_buffer()
    for i in range(len(im)):
        row = ['.'] * width
        row += deepcopy(im[i])
        row += ['.'] * width
        im_out.append(row)
    append_vertical_buffer()
    return im_out

def enhance_n_times(image, algo, times):
    # first add a border of width times + 1
    enhanced = add_border(image, times + 1)
    for i in range(times):
        enhanced = enhance_image(enhanced, algo)
    return enhanced

def count_lit_pixels(image):
    return sum(sum(1 for pixel in im_row if pixel == '#') for im_row in image)

def main():
    algo = '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##'
    image = ['#..#.','#....','##..#','..#..','..###']
    assert get_enhanced_pixel(image, algo, 2, 2) == '#'

    with open('example_input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    assert count_lit_pixels(enhance_n_times(lines[2:], lines[0], 1)) == 24
    assert count_lit_pixels(enhance_n_times(lines[2:], lines[0], 2)) == 35
    assert count_lit_pixels(enhance_n_times(lines[2:], lines[0], 50)) == 3351

    with open('input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    assert count_lit_pixels(enhance_n_times(lines[2:], lines[0], 2)) == 4964
    print(count_lit_pixels(enhance_n_times(lines[2:], lines[0], 50)))

if __name__ == "__main__":
	main()
