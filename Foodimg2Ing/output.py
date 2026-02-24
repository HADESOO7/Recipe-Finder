import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import numpy as np
import os
from Foodimg2Ing.args import get_parser
import pickle
from Foodimg2Ing.model import get_model
from torchvision import transforms
from Foodimg2Ing.utils.output_utils import prepare_output
from PIL import Image
import time
from tensorflow.keras.preprocessing import image
from Foodimg2Ing import app
import torchvision.models as models
import sys
import copy

# Global variables for caching models to avoid reloading them on each request
_recipe_model = None
_classifier_model = None
_ingrs_vocab = None
_instr_vocab = None
_device = None

def _get_models():
    global _recipe_model, _classifier_model, _ingrs_vocab, _instr_vocab, _device
    
    # Return immediately if models are already loaded
    if _recipe_model is not None:
        return _recipe_model, _classifier_model, _ingrs_vocab, _instr_vocab, _device

    data_dir = os.path.join(app.root_path, 'data')
    use_gpu = True
    _device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
    map_loc = None if torch.cuda.is_available() and use_gpu else 'cpu'

    _ingrs_vocab = pickle.load(open(os.path.join(data_dir, 'ingr_vocab.pkl'), 'rb'))
    _instr_vocab = pickle.load(open(os.path.join(data_dir, 'instr_vocab.pkl'), 'rb'))

    # Safely isolate argv when parsing arguments configuration
    old_argv = copy.copy(sys.argv)
    sys.argv = ['']
    args = get_parser()
    sys.argv = old_argv
    
    args.maxseqlen = 15
    args.ingrs_only = False
    
    _recipe_model = get_model(args, len(_ingrs_vocab), len(_instr_vocab))
    model_path = os.path.join(data_dir, 'modelbest.ckpt')
    _recipe_model.load_state_dict(torch.load(model_path, map_location=map_loc))
    _recipe_model.to(_device)
    _recipe_model.eval()
    _recipe_model.ingrs_only = False
    _recipe_model.recipe_only = False

    _classifier_model = models.resnet18(pretrained=True).to(_device).eval()

    return _recipe_model, _classifier_model, _ingrs_vocab, _instr_vocab, _device

def output(uploadedfile):
    # Fetch cached models
    model, classifier, ingrs_vocab, vocab, device = _get_models()

    transf_list_batch = [
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ]
    to_input_transf = transforms.Compose(transf_list_batch)

    greedy = [True, False]
    beam = [-1, -1]
    temperature = 1.0
    numgens = len(greedy)

    img = image.load_img(uploadedfile)
    show_anyways = True
    
    transf_list = [
        transforms.Resize(256),
        transforms.CenterCrop(224)
    ]
    transform = transforms.Compose(transf_list)
    
    image_transf = transform(img)
    image_tensor = to_input_transf(image_transf).unsqueeze(0).to(device)

    # Pre-check: Is it a food image?
    try:
        with torch.no_grad():
            preds = classifier(image_tensor)
            top5 = torch.topk(preds, 5)[1].squeeze().tolist()
        
        # ImageNet food indices roughly 923-969
        food_indices = set(range(923, 970))
        is_food = any(idx in food_indices for idx in top5)
    except:
        is_food = True

    num_valid = 1
    title = []
    ingredients = []
    recipe = []

    if not is_food:
        for i in range(numgens):
            title.append("Not a food image!")
            ingredients.append(["None"])
            recipe.append(["Please upload a valid picture of food. Your image doesn't seem to contain any recognizable dishes."])
        return title, ingredients, recipe

    for i in range(numgens):
        with torch.no_grad():
            outputs = model.sample(image_tensor, greedy=greedy[i], 
                                temperature=temperature, beam=beam[i], true_ingrs=None)
                
        ingr_ids = outputs['ingr_ids'].cpu().numpy()
        recipe_ids = outputs['recipe_ids'].cpu().numpy()
                
        outs, valid = prepare_output(recipe_ids[0], ingr_ids[0], ingrs_vocab, vocab)
            
        if valid['is_valid'] or show_anyways:
            title.append(outs['title'])
            ingredients.append(outs['ingrs'])
            recipe.append(outs['recipe'])
        else:
            title.append("Not a valid recipe!")
            recipe.append("Reason: " + valid['reason'])
            
    return title, ingredients, recipe
