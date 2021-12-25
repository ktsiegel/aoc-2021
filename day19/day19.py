from copy import deepcopy

def parse_scanner_results(lines):
    scanners = []
    curr_scanner = ''
    curr_beacons = []
    for line in lines:
        if len(line.strip()) == 0:
            if len(scanners) == 0:
                scanners.append((curr_scanner, curr_beacons, True))
            else:
                scanners.append((curr_scanner, curr_beacons, False))
            curr_beacons = []
            continue
        if line[:3] == '---':
            curr_scanner = line.strip()
        else:
            curr_beacons.append(tuple([int(x) for x in line.strip().split(',')]))
    scanners.append((curr_scanner, curr_beacons, False))
    return scanners

def get_transformation_fns():
    transformation_fns = []
    axes_transforms = [ \
        lambda pt: pt, # (x,y,z)
        lambda pt: (-1*pt[0], pt[1], -1*pt[2]), # (-x, y, -z)
        lambda pt: (pt[1], pt[2], pt[0]), # (y, z, x)
        lambda pt: (-1*pt[1], -1*pt[0], -1*pt[2]), # (-y, -x, -z)
        lambda pt: (pt[2], pt[1], -1*pt[0]),  # (z, y, -x)
        lambda pt: (-1*pt[2], pt[1], pt[0])] # (-z, y, x)
    for axes_transform in axes_transforms:
        yz_rotations = [ \
            lambda pt: pt,
            lambda pt: (pt[0], pt[2], -1*pt[1]), # (x, z, -y)
            lambda pt: (pt[0], -1*pt[2], pt[1]), # (x, -z, y)
            lambda pt: (pt[0], -1*pt[1], -1*pt[2])] # (x, -y, -z)
        for yz_rotation in yz_rotations:
            transformation_fns.append([axes_transform, yz_rotation])
    return transformation_fns
TRANSFORMATION_FNS = get_transformation_fns()

def apply_transform(fn, pt):
    return fn[1](fn[0](pt))

def get_translation_fn(pt1, pt2):
    return lambda pt: (pt2[0]-pt1[0]+pt[0], pt2[1]-pt1[1]+pt[1], pt2[2]-pt1[2]+pt[2])

# translate b2 to b1 and check for shared beacons
def check_overlap(b1, b2):
    b1_pts = set(b1)
    for pt1_idx in range(len(b1)):
        pt1 = b1[pt1_idx]
        for pt2_idx in range(len(b2)):
            pt2 = b2[pt2_idx]
            translate = get_translation_fn(pt2, pt1) # transformation to get from pt2 to pt1
            # translate the rest of the points to see if 12 total match
            overlap = [pt1]
            for trans_idx in range(len(b2)):
                if pt2_idx == trans_idx:
                    continue
                translated_pt = translate(b2[trans_idx])
                if translated_pt in b1_pts:
                    overlap.append(translated_pt)
            if len(overlap) >= 12:
                return overlap, translate
    return [], None

def count_unique_beacons(scanners):
    beacons = set()
    for [name, scanner_beacons, _] in scanners:
        for sb in scanner_beacons:
            beacons.add(sb)
    return len(beacons)

def calc_manhattan(pt1, pt2):
    return abs(pt2[0]-pt1[0]) + abs(pt2[1]-pt1[1]) + abs(pt2[2]-pt1[2])

def max_manhattan_distance(pts):
    max_manhattan = 0
    for i in range(len(pts)):
        for j in range(len(pts)):
            if i == j:
                continue
            max_manhattan = max(max_manhattan, calc_manhattan(pts[i], pts[j]))
    return max_manhattan

def solve(lines):
    scanners = parse_scanner_results(lines)
    already_checked = set()
    to_check = [0]
    relative_pts = [None] * len(scanners)
    relative_pts[0] = (0,0,0)
    # for each pair of beacons
    while len(to_check) > 0:
        i = to_check.pop(0)
        if i in already_checked:
            continue
        already_checked.add(i)
        for j in range(len(scanners)):
            if i == j or scanners[j][2]:
                continue
            # for every beacon detected by scanner j, check every transformation of points
            for t_idx in range(len(TRANSFORMATION_FNS)):
                t_fn = TRANSFORMATION_FNS[t_idx]
                t_pts = []
                for pt in scanners[j][1]:
                    t_pts.append(apply_transform(t_fn, pt))
                overlap, translate = check_overlap(scanners[i][1], t_pts)
                if len(overlap) >= 12:
                    # translate all points to this new coordinate system and replace its entry in scanners
                    # scanners[i] underwent rotation t_idx and then translate to get to scanners[j]
                    # so scanners[j] has to go through the inverse
                    print('{} relative to {}. overlap: {}, transform: {}, center of j: {}'.format(scanners[j][0], scanners[i][0], len(overlap), t_idx, translate((0,0,0))))
                    new_j_pts = []
                    for j_pt in t_pts:
                        new_j_pts.append(translate(j_pt))
                    scanners[j] = (scanners[j][0], new_j_pts, True)
                    to_check.append(j)
                    relative_pts[j] = translate((0,0,0))
    return count_unique_beacons(scanners), max_manhattan_distance(relative_pts)


def main():
    with open('input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    print(solve(lines))

if __name__ == "__main__":
	main()















