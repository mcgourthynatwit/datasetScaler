import os
from fastai.vision.all import *

def modelMaker(directory, model_directory):   

        print("Creating datablock model...")
        data_block = DataBlock(
            blocks=(ImageBlock, CategoryBlock),
            get_items=get_image_files,
            splitter=RandomSplitter(valid_pct=0.25, seed=30),
            get_y=parent_label,
            item_tfms=Resize(128, method = 'pad')
        )

        print("Loading data into datablock...")
        dataLoad = data_block.new(item_tfms=RandomResizedCrop(224, min_scale=0.5),batch_tfms=aug_transforms())
        dls = dataLoad.dataloaders(directory, bs = 100, num_workers = 0)
        dls.one_batch()

        print("Loading pre-trained recognition model...")
        learn = load_learner(r"C:\Users\mcgourthyn\Pictures\model.pkl") # model path
        learn.dls = dls
        
        n_out = len(dls.vocab)
        learn.model[1][8] = nn.Linear(512, n_out).cuda()
        learn.loss_func = CrossEntropyLossFlat()

        print("Fine tuning model...")
        learn.fine_tune(1, base_lr=3e-3, freeze_epochs=6, cbs=EarlyStoppingCallback(monitor='valid_loss', min_delta=0.01, patience=3))

        print("Model fine tuned, saving model...")
        model = os.path.join(model_directory, "model.pkl")
        learn.export(model)        
        print("Model created and saved !")

                       
        return model, model_directory
             
        
    
 

    
