"""
bulk parallel mp4 to wav conversion
parallelism only supported for linux at the moment
"""
import glob, os, tqdm
import multiprocessing


seg_ids_for_conv = [1, 2, 3, 4]

# split the list conversion in multiple segs 0 to 60k, 60k to 120k and so on
RANGE_GAP = 60000

all_mp4_paths = []
print("processing segments")
for seg in tqdm.tqdm(seg_ids_for_conv):
    seg_path = f"seg_{seg}/*/*.mp4"
    all_mp4_paths.extend(glob.glob(seg_path))

print(f"Total mp4 found: {len(all_mp4_paths)}")

all_ffmpeg_task_list = [] # for parallel execution
print("building ffmpeg task list for parallel exec.")
for mp4 in tqdm.tqdm(all_mp4_paths):
    wav_path = mp4.replace(".mp4", ".wav")
    if not os.path.isfile(wav_path): # only add to task list if not present already
        cmd = f"ffmpeg -i {mp4} -vn -ar 16000 -ac 1 {wav_path}\n"
        all_ffmpeg_task_list.append(cmd) # ffmpeg conversion cmd

print(f"Total wav files: {len(all_ffmpeg_task_list)}")

print("writing the task list")
task = open("tasks", "w")
for t in all_ffmpeg_task_list:
    task.write(t)

cpu_c = multiprocessing.cpu_count()
print(f"number of cpu cores: {cpu_c}")

task.close()

print("executing the tasks with gnu parallel")
os.system(f"parallel --jobs {cpu_c} < tasks") # if this one fails manually run this under tmux

