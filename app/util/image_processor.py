import numpy as np
from PIL import Image
from typing import Literal
import random
import os


from app import canvas_np_img_to_png, downscale_img, ASSETS_DIR

class ImageProcessor:
    def __init__(self):
        self.lowest_varience = 100
        self.output_variance = -1
        self.best_image_index = -1
        self.tolerance = .5
        self.previous_matchs = []
        self.prev_match_range = 1
        self.prev_matchs_list_size = 100
        pass
        
    
    def get_variance(self):
        return self.output_variance * 1000
        
    def set_tolerance_dict(self, tolerances:dict):
        self.tolerance_dict = tolerances
        pass
    
    def set_data(self, dataset_4: str, dataset_8:str, dataset_16:str, dataset_32:str, dataset_64:str, dataset_128:str):
        self.dataset4 = np.load(dataset_4)
        self.dataset8 = np.load(dataset_8)
        self.dataset16 = np.load(dataset_16)
        self.dataset32 = np.load(dataset_32)
        self.dataset64 = np.load(dataset_64)
        self.dataset128 = np.load(dataset_128)
        self.max_index = self.dataset128.shape[0]
        pass



    
    def dataset_error_check(self, d1, d2):
        d1_shape_0 = d1.shape[0]
        d2_shape_0 = d2.shape[0]
        if d1_shape_0 != d2_shape_0:
            print("ERROR: img_processing \n dataset error! Datasets are of different sizes")
            if d1_shape_0 < d2_shape_0:
                self.max_index = d1_shape_0
            else:
                self.max_index = d2_shape_0
            print(f"New max index = {self.max_index}")
        

    def compare_img_with_downscaled_data_set(self, input_image, type: Literal['any', 'line', 'shape']):
        self.type = type
        
        input64 = downscale_img(input_image)
        input32 = downscale_img(input64)
        input16 = downscale_img(input32)
        input8 = downscale_img(input16)
        input4 = downscale_img(input8)

        index_list = [(i, 10) for i in range(self.max_index)]
        temp_index_list = []

        #Enumerate each downscaled depth 
        #4x4 
        temp_index_list.clear()
        index_list = self.compare_input_to_dataset(index_list, self.dataset4, input4, True, self.tolerance_dict['threshold4'])
        #8x8
        temp_index_list.clear()
        index_list = self.compare_input_to_dataset(index_list, self.dataset8, input8, False, self.tolerance_dict['threshold8'])
        #16x16
        temp_index_list.clear()
        index_list = self.compare_input_to_dataset(index_list, self.dataset16, input16, False, self.tolerance_dict['threshold16'])
        #32x32
        temp_index_list.clear()
        index_list = self.compare_input_to_dataset(index_list, self.dataset32, input32, False, self.tolerance_dict['threshold32'])
        #64x64
        temp_index_list.clear()
        index_list = self.compare_input_to_dataset(index_list, self.dataset64, input64, False, self.tolerance_dict['threshold64'])
        #128x128
        temp_index_list.clear()
        index_list = self.compare_input_to_dataset(index_list, self.dataset128, input_image, False, self.tolerance_dict['threshold128'])

        print(f"\n\nFinal Input List Size = {len(index_list)}. ")
        #output_index = self.best_image_index
        output_index = random.choice(index_list)
        output_index = output_index[0]

        self.previous_matchs.append(output_index)
        if len(self.previous_matchs) > self.prev_matchs_list_size : 
            self.previous_matchs = self.previous_matchs[1:]

        sim_img_assets_path = os.path.join(ASSETS_DIR, "similar-images")

        canvas_np_img_to_png(self.dataset128[output_index,0,:], "similar128.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset128[output_index,1,:], "similar_stroke.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset4[output_index,0,:], "similar4.png", sim_img_assets_path)
        canvas_np_img_to_png(input4, "input4.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset8[output_index,0,:], "similar8.png", sim_img_assets_path)
        canvas_np_img_to_png(input8, "input8.png",sim_img_assets_path)
        canvas_np_img_to_png(self.dataset16[output_index,0,:], "similar16.png", sim_img_assets_path)
        canvas_np_img_to_png(input16, "input16.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset32[output_index,0,:], "similar32.png", sim_img_assets_path)
        canvas_np_img_to_png(input32, "input32.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset64[output_index,0,:], "similar64.png", sim_img_assets_path)
        canvas_np_img_to_png(input64, "input64.png", sim_img_assets_path)
        return self.dataset128[output_index, 1, :]



    def compare_input_to_dataset(self, index_list: list, dataset: np.array, input_img: np.array, first_run: bool, tolerance: int):
        lowest_variance = 1000000.0
        best_index = 0
        temp_index_list = []
        tolerance_modified = tolerance* .0001 - .0001
        for index, value in index_list:
            skip_data = False
            if first_run:
                skip_data = prev_match_check(index, self.previous_matchs, self.prev_match_range)
                tolerance_modified *= 1.0005
            if skip_data == False:
                dataset_element = dataset[index, 0 , :]
                variance = compare_two_images(input_img, dataset_element)
                edge_to_shape_ratio = dataset[index, 1 , :][-1]
                if self.type == 'line':
                    if edge_to_shape_ratio > .55:
                        variance -= .1
                    else:
                        variance += .1
                if self.type == 'shape':
                    if edge_to_shape_ratio <= .55:
                        variance -= .1
                    else:
                        variance += .1
                

                if variance < lowest_variance:
                    lowest_variance = variance
                    best_index = index
                if variance <= lowest_variance + tolerance_modified:
                    temp_index_list.append((index, variance))
        max_variance = lowest_variance + tolerance_modified
        print(f"TempList Length = {len(temp_index_list)}")
        output_index_list = trim_data_set(temp_index_list, max_variance)
        print(f"Lowest Variance = {lowest_variance}. Index = {best_index}")
        self.best_image_index = best_index
        self.output_variance = lowest_variance
        return output_index_list


def trim_data_set(input_list, max_variance):
    index_variance_list = []
    for maybe_img, maybe_variance in input_list:
            if maybe_variance <= max_variance:
                index_variance_list.append((maybe_img, maybe_variance))
    return index_variance_list


def compare_two_images(img1, img2):
        img1_shape = img1.shape[0]

        #check if same shape
        if (img1_shape != img2.shape[0]):
            print(f"\n Error: img_processor,  compare_two_images() \n img1 != img 2 \n img1 = {img1.shape} \n img2 = {img2.shape}")
            return -1

        diff_array = np.abs(img1 - img2)
        diff = np.sum(diff_array)
        variance = diff / img1_shape
        return variance

def prev_match_check(input_index, prev_match_list, drop_range):
    skip_data = False
    for old_match in prev_match_list:
        for x in range(drop_range):
            if input_index == old_match:
                skip_data = True
            if input_index == old_match + x:
                #print(f"Skipping element {index}. Index allready used recently")
                skip_data = True
            if input_index == old_match - x:
                #print(f"Skipping element {index}. Index allready used recently")
                skip_data = True
    return skip_data