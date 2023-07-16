import DataModelMaker
import multiprocessing as mp
import FolderScaler as fs
if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    DataModelMaker.modelMaker(r"C:\Users\mcgourthyn\Pictures\images") # need to change this if you want to run
    # folder must have atleast two nested folders each containing 10 images