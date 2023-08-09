from fastai.vision.all import *
from functions.make_model_folder import makeModelFolderDirectory
import folder_scaler as fs

# Specify path to Caltech-101 dataset
path_caltech = Path(r"C:\Users\mcgourthyn\Pictures\caltech-101")

model_directory = makeModelFolderDirectory(path_caltech, "modelName") # this line will be changed after testing
fs.folderScaler(model_directory)
print("model folder scaled")

print("Loading images into model")
fns = get_image_files(model_directory)
print(fns)

# Create a DataBlock and DataLoaders
print("Creating datablock model")
data_block = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.65, seed=30),
    get_y=parent_label,
    item_tfms=Resize(128, method = 'pad')
)
print("Loading data into datablock")
dataLoad = data_block.new(item_tfms=RandomResizedCrop(224, min_scale=0.5),batch_tfms=aug_transforms())
dls = dataLoad.dataloaders(path_caltech, bs = 100, num_workers = 0)
dls.one_batch()
print("Testing model")
learn = vision_learner(dls, resnet34, metrics=error_rate)

print("Find tuning model")
learn.fine_tune(1, base_lr=3e-3, freeze_epochs=6, cbs=EarlyStoppingCallback(monitor='valid_loss', min_delta=0.01, patience=3))

# Save the trained model
model = os.path.join(model_directory, "model.pkl")
learn.export(model)        
print("Model created and saved")
