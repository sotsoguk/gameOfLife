import sys, argparse
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]
vals_p = [0.2, 0.8]


def readPattern(pattern_file):
	pattern_lines = []
	with open(pattern_file,'r') as f:
		pattern_lines = f.readlines()

	cols = int(pattern_lines[0])
	rows = int(pattern_lines[1])
	pattern = np.zeros(cols*rows).reshape(rows, cols)
	for i in range(2,rows+2):
		
		entries = pattern_lines[i].split()
		for j in range(0,cols):
			
			if entries[j] == '0':
				pattern[i-2,j] = OFF
			else:
				pattern[i-2,j] = ON
				
		
	print np.size(pattern, axis=1)
	return pattern

def addPattern(pattern, i,j,grid):
	pattern_width = np.size(pattern, axis=1)
	pattern_height = np.size(pattern, axis=0)
	n = np.size(grid,axis=0)
	if pattern_height+i > n or pattern_width+j > n:
		print "Pattern 2 Big!"
		exit(0)
	grid[i:i+pattern_height,j:j+pattern_width] = pattern
	

def randomGrid(N):
	return np.random.choice(vals, N*N, vals_p).reshape(N,N)

def addGlider(i, j, grid):
	 glider = np.array([[0,    0, 255],
                                    [255,  0, 255],
                                    [0,  255, 255]])
	 grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N):
	newGrid = grid.copy()
	for i in range(N):
		for j in range(N):
			total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                                      grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                                      grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                                      grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
			# apply conways rules
			if grid[i, j] == ON:
				if (total < 2) or (total > 3):
					newGrid[i, j] = OFF
			else:
				if total == 3:
					newGrid[i, j] = ON
	img.set_data(newGrid)
	grid[:] = newGrid[:]
	return img

def main():
	# pattern = readPattern('gosper.pat')
	# grid = randomGrid(100)
	# addPattern(pattern, grid)
	# exit(0)

	parser = argparse.ArgumentParser(description="Conway's Game Of Life :)")
	parser.add_argument('--grid-size',dest='N', required = False)
	parser.add_argument('--mov-file', dest='movfile', required=False)
	parser.add_argument('--interval',dest='interval', required=False)
	parser.add_argument('--glider', action='store_true', required = False)
	parser.add_argument('--pattern', dest='pattern_file', required = False)

	args = parser.parse_args()

	N=100
	if args.N and int(args.N) > 8:
		N = int(args.N)

	

	# interval
	updateInterval = 50
	if args.interval:
		updateInterval = int(args.interval)
	
	if args.pattern_file:
		pattern = readPattern(args.pattern_file)
		grid = np.zeros(N*N).reshape(N,N)
		addPattern(pattern,1,1,grid)
	elif args.glider:
		grid = np.zeros(N*N).reshape(N, N)
		addGlider(1,1,grid)
	else:
		grid = randomGrid(N)
	# setup animation
	fig, ax = plt.subplots()
	img = ax.imshow(grid, interpolation = 'nearest')
	ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,), frames = 10, interval = updateInterval, save_count = 50)
	if args.movfile:
		ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
	plt.show()

if __name__ == '__main__':
	main()