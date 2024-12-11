import numpy as np
from PIL import Image
import random
import os


from app import canvas_np_img_to_png, downscale_img, ASSETS_DIR

class ImageProcessor:
    def __init__(self, data_set_128_file: str = None, data_set_64_file: str = None, data_set_32_file: str = None,
                  data_set_16_file: str = None, data_set_8_file: str= None, data_set_4_file: str = None, input_data = None):
        
        self.downscaled_data  = []
        if data_set_128_file != None:
            self.dataset_128 = np.load(data_set_128_file)
            self.downscaled_data.append(self.dataset_128)
            self.max_index = self.dataset_128.shape[0]
            print(f"Data Set of shape {self.dataset_128.shape} Loaded")

        if data_set_64_file != None:
            self.dataset_64 = np.load(data_set_64_file)
            self.downscaled_data.append(self.dataset_64)
            self.dataset_error_check(self.dataset_128, self.dataset_64)
        else:
            self.downscaled_data.append(-1)

        if data_set_32_file != None:
            self.dataset_32 = np.load(data_set_32_file)
            self.downscaled_data.append(self.dataset_32)
            self.dataset_error_check(self.dataset_128, self.dataset_32)
        else:
            self.downscaled_data.append(-1)
            
        if data_set_16_file != None:
            self.dataset_16 = np.load(data_set_16_file)
            self.downscaled_data.append(self.dataset_16)
            self.dataset_error_check(self.dataset_128, self.dataset_16)
        else:
            self.downscaled_data.append(-1)
            
        if data_set_8_file != None:
            self.dataset_8 = np.load(data_set_8_file)
            self.downscaled_data.append(self.dataset_8)
            self.dataset_error_check(self.dataset_128, self.dataset_8)
        else:
            self.downscaled_data.append(-1)
            
        if data_set_4_file != None:
            self.dataset_4 = np.load(data_set_4_file)
            self.downscaled_data.append(self.dataset_4)
            self.dataset_error_check(self.dataset_128, self.dataset_4)
        else:
            self.downscaled_data.append(-1)
        
        self.downscaled_data_depth = len(self.downscaled_data)
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
        
    def set_tolerance(self, t):
        self.tolerance = t*.0001 - .0001
        pass
    
    def set_data(self, dataset_4: str, dataset_8:str, dataset_16:str, dataset_32:str, dataset_64:str, dataset_128:str):
        self.dataset_4 = np.load(dataset_4)
        self.dataset_8 = np.load(dataset_8)
        self.dataset_16 = np.load(dataset_16)
        self.dataset_32 = np.load(dataset_32)
        self.dataset_64 = np.load(dataset_64)
        self.dataset_128 = np.load(dataset_128)
        self.downscaled_data = [self.dataset_128, self.dataset_64, self.dataset_32, self.dataset_16, self.dataset_8, self.dataset_4]
        self.downscaled_data_depth = len(self.downscaled_data)
        self.max_index = self.dataset_128.shape[0]
        pass

    def set_downscaled_data(self, downscaled_data_paths: list):
        '''Sets downscaled data. Recieves a list like:
          [d128_path, d64_path, d32_path, d16_path, d8_path, d4_path]'''
        downscaled_data = []
        for path in downscaled_data_paths:
            ds = np.load(path)
            downscaled_data.append(ds)
        self.downscaled_data = downscaled_data
        self.downscaled_data_depth = len(self.downscaled_data)
        self.max_index = self.downscaled_data[0].shape[0]
        pass

    def set_data_set(self, ds):
        #FOR DELETION PROB GET RID OF 
        self.dataset_128 = np.load(ds)
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
        

    def compare_img_with_downscaled_data_set(self, input_image):
        input_img_ds1 = downscale_img(input_image)
        input_img_ds2 = downscale_img(input_img_ds1)
        input_img_ds3 = downscale_img(input_img_ds2)
        input_img_ds4 = downscale_img(input_img_ds3)
        input_img_ds5 = downscale_img(input_img_ds4)
        input_ds_list = [input_image, input_img_ds1, input_img_ds2, input_img_ds3, input_img_ds4, input_img_ds5]

        index_list = [(i, 10) for i in range(self.max_index)]
        temp_index_list = []
        first_run = True
        
        if len(input_ds_list) != self.downscaled_data_depth:
            print(f"\nError: img_process    compare_img_with_downscaled_data_set() \n input downscaled to a diffrent depth as dataset\n input depth = {len(input_ds_list)} \n dataset depth = {self.downscaled_data_depth}")

        #Enumerate each downscaled depth 

        for ds_level in range(self.downscaled_data_depth - 1, -1, -1):
            input_img_scaled = input_ds_list[ds_level]
            dataset_ds_level = self.downscaled_data[ds_level]
            temp_index_list.clear()

            print(f"\nFinding Matches at downscaled depth = {ds_level}. Iterating over index list of length {len(index_list)}")
            print(f"Dataset Shape = {dataset_ds_level.shape}")
            print(f"Input IMG shape = {input_img_scaled.shape}")

            index_list = self.compare_input_to_dataset(index_list, dataset_ds_level, input_img_scaled, first_run)
            first_run = False
        
        print(f"\n\nFinal Input List Size = {len(index_list)}. ")
        #output_index = self.best_image_index
        output_index = random.choice(index_list)
        output_index = output_index[0]

        self.previous_matchs.append(output_index)
        if len(self.previous_matchs) > self.prev_matchs_list_size : 
            self.previous_matchs = self.previous_matchs[1:]

        sim_img_assets_path = os.path.join(ASSETS_DIR, "similar-images")

        canvas_np_img_to_png(self.dataset_128[output_index,0,:], "similar128.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset_128[output_index,1,:], "similar_stroke.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset_4[output_index,0,:], "similar4.png", sim_img_assets_path)
        canvas_np_img_to_png(input_img_ds5, "input4.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset_8[output_index,0,:], "similar8.png", sim_img_assets_path)
        canvas_np_img_to_png(input_img_ds4, "input8.png",sim_img_assets_path)
        canvas_np_img_to_png(self.dataset_16[output_index,0,:], "similar16.png", sim_img_assets_path)
        canvas_np_img_to_png(input_img_ds3, "input16.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset_32[output_index,0,:], "similar32.png", sim_img_assets_path)
        canvas_np_img_to_png(input_img_ds2, "input32.png", sim_img_assets_path)
        canvas_np_img_to_png(self.dataset_64[output_index,0,:], "similar64.png", sim_img_assets_path)
        canvas_np_img_to_png(input_img_ds1, "input64.png", sim_img_assets_path)
        return self.dataset_128[output_index, 1, :]



    def compare_input_to_dataset(self, index_list, dataset, input_img, first_run):
        lowest_variance = 1000000.0
        best_index = 0
        temp_index_list = []
        t = self.tolerance
        for index, v in index_list:
            skip_data = False
            if first_run:
                skip_data = prev_match_check(index, self.previous_matchs, self.prev_match_range)
                t *= 1.0005
            if skip_data == False:
                dataset_element = dataset[index, 0 , :]
                variance = compare_two_images(input_img, dataset_element)
                if variance < lowest_variance:
                    lowest_variance = variance
                    best_index = index
                if variance <= lowest_variance + t:
                    temp_index_list.append((index, variance))
        max_variance = lowest_variance + t
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