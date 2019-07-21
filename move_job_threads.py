import shutil
from timeloop import Timeloop
from datetime import timedelta
from GUI import showinfo
from write_log import write_to_file as w_to_f
AUTO_MOVE = True
DEFAULT_INTERVAL = 20
DEFAULT_THREADS = 1
move_thread = Timeloop()


def create_threads(source_path, destination_path, file_list):
    thread_count = len(file_list)/100 + 1

    @move_thread.job(interval=timedelta(seconds=DEFAULT_INTERVAL))
    def move_file():
        errors = ''
        flag = False
        for f in file_list:
            try:
                shutil.move(source_path + '/' + str(f), destination_path)
                # Using write_log module to save log of moved files
                w_to_f(str(f+','+source_path+','+destination_path))
            except shutil.Error as err:
                errors += str(err.args[0]) + '\n'
                flag = True
        if flag:
            showinfo("Errors:", errors)

    if AUTO_MOVE:
        move_thread.start(block=True)



