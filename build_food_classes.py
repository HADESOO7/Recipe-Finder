import torchvision.models as models
import torchvision.transforms as transforms
import torch
from setuptools import setup
import urllib.request
from PIL import Image

def build_food_classifier():
    # Download ImageNet classes
    try:
        url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        urllib.request.urlretrieve(url, "imagenet_classes.txt")
    except:
        pass

    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]
    
    # Let's print out all categories and we can manually inspect or use a heuristic
    food_keywords = ['fruit', 'vegetable', 'meat', 'dish', 'plate', 'bowl', 'cup', 'bottle', 'food', 'bread', 'cake', 'soup', 'pizza', 'burger', 'sandwich', 'hotdog', 'cheese', 'salad', 'apple', 'orange', 'banana', 'strawberry', 'lemon', 'mushroom', 'corn', 'squash', 'pepper', 'onion', 'garlic', 'potato', 'bean', 'nut', 'seed', 'egg', 'fish', 'chicken', 'beef', 'pork', 'lobster', 'crab', 'shrimp', 'squid', 'octopus', 'ice cream', 'chocolate', 'candy', 'cookie', 'pie', 'pasta', 'noodle', 'rice', 'wine', 'beer', 'coffee', 'tea', 'juice', 'milk', 'water', 'oil', 'sauce', 'spice', 'herb', 'salt', 'sugar', 'flour', 'butter', 'margarine', 'yogurt', 'cream', 'honey', 'jam', 'jelly', 'peanut', 'almond', 'walnut', 'pecan', 'cashew', 'pistachio', 'macadamia', 'hazelnut', 'chestnut', 'coconut', 'avocado', 'tomato', 'cucumber', 'lettuce', 'spinach', 'cabbage', 'broccoli', 'cauliflower', 'carrot', 'radish', 'turnip', 'beet', 'celery', 'asparagus', 'artichoke', 'eggplant', 'zucchini', 'pumpkin', 'melon', 'watermelon', 'grape', 'cherry', 'peach', 'plum', 'apricot', 'pear', 'fig', 'date', 'pomegranate', 'pineapple', 'papaya', 'mango', 'guava', 'kiwi', 'lychee', 'passion fruit', 'dragon fruit', 'starfruit', 'persimmon', 'quince', 'cranberry', 'blueberry', 'raspberry', 'blackberry', 'currant', 'gooseberry', 'elderberry', 'mulberry', 'boysenberry', 'loganberry', 'salmonberry', 'cloudberry', 'huckleberry', 'marionberry', 'tayberry', 'lingonberry', 'strawberry', 'acai', 'goji', 'acerola', 'camu camu', 'lucuma', 'maca', 'mesquite', 'hemp', 'chia', 'flax', 'quinoa', 'amaranth', 'buckwheat', 'millet', 'sorghum', 'teff', 'oat', 'barley', 'rye', 'wheat', 'spelt', 'kamut', 'farro', 'bulgur', 'couscous', 'polenta', 'grits', 'cornmeal', 'masa']
    
    food_indices = []
    for i, cat in enumerate(categories):
        cat_lower = cat.lower()
        # Some are known food indices
        if 923 <= i <= 969: # Food & dishes in ImageNet
            food_indices.append(i)
            continue
        if 935 <= i <= 955: # Fruits and veg
            food_indices.append(i)
            continue
            
        for kw in food_keywords:
            if kw in cat_lower:
                food_indices.append(i)
                break
                
    return set(food_indices), categories

if __name__ == "__main__":
    indices, cats = build_food_classifier()
    print("Found", len(indices), "food categories.")
    print("Some food categories:", [cats[i] for i in list(indices)[:20]])
