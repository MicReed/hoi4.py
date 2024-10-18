import cProfile
import pstats
from tqdm import tqdm

def check_profile(n_lines):
    def check_profile(func):
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            result = profiler.runcall(func, *args, **kwargs)
            stats = pstats.Stats(profiler)
            stats.sort_stats("tottime")
            stats.print_stats(n_lines)
            return result
        return wrapper
    return check_profile



t_range = 10
step = 1
from tqdm import tqdm
import time

# Create a progress bar with 100 total units
pbar = tqdm(total=100)

# Simulate a process that updates the progress bar
for i in range(100):
    time.sleep(0.1)  # Simulate work by sleeping for 0.1 seconds
    pbar.n = i  # Set the progress bar to the current value of i
    pbar.refresh()  # Refresh the progress bar to show the update

pbar.close()  # Close the progress bar when done