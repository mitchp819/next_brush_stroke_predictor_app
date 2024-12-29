# Next Brush Stroke Predictor 
Description: 

## Instilation
Install dependencies: pip install -r requirements.txt

# About

## Terminology 

- **Dataset**: A collection of canvas, brush stroke pairs. 
- **Database**: Are Folders where **Datasets** and **Compiled Data** live.
    - final_image (sub folder): Holds png images of the final canvas for each dataset. Images are given an id which corresponds to the id on their related dataset located in the image_data folder. 
    - gen_data (sub folder): When a Database is compiled the resulting numpy arrays live here. 
    - image_data (sub folder): Home to **Datasets** saved to the given database. **Datasets** are given an id which correspond to their related dataset located in the final_image folder.
- **Compiled Data**: When a **Database** is compiled Data is prepared for Generation. Data is concatenated into a master numpy array and then downscaled to each scale {126x128, 64x64, 32x32, 16x16, 8x8, 4x4}

## Widgets

##### Main Window

- **Brush Tool**: Allows users to configure their brush.
    - Brush Size Slider: A slider from 1 - 50 defining the size of the brush.
    - Brush Greyscale Slider: A slider from 0 - 255 defining the Hue of the greyscale value. Where 0 represents black and 255 represents white. 
    - Sample Brush Stroke: Updates a sample brush stroke when the Brush Size Slider or the Brush Grey Scale Slider are modified by the user. 
- **Canvas**: The drawing canvas accepts input defined by the **Brush Tool**. The size of the Canvas is 128x128 pixels but the Canvas is scaled to your screen size. 
- **Threshold Slider**: The threshold slider defines  how close the generated brush stroke is to the input. A higher threshold will produce more random outputs. 
    - Threshold by scale: Under Advanced Thresholding the user can modify the thresholds for each scale of input to data element comparison. A high threshold will essentially turn that scale 'Off'. A low threshold will weed out more elements increase a given scales importants. *Tip: a low threshold at smaller scales and a high threshold at larger scales will generate outputs with more generalization.*
- **Console**: Documents events. 
- **Info Pane**: Includes text and images related to the configured settings and the generated input output. 

##### Config Data Window

- **Generator Database Selector**: Select a single database to generate brushstrokes from
- **Save To Database Selector**: Select one or more databases to save data

## Buttons 
 
 ##### Main Window
 - **Save Image**: Saves the current Canvas as a png to the folder 'saved-images'. 
 - **Save Dataset**: Saves the active dataset to a database 
 - **Data Gather Mode**: Switch between modes 'Auto' and 'Manual'.
    - 'Auto' mode automatically saves each brush strokes to a dataset. When the mouse button is released the brush stroke will be saved. 
    - 'Manual' mode allows the user to specify what a brush stroke is. Users can make multiple strokes. Only when the **Save Brush Stroke** button is clicked will data be saved to the dataset. 
- **Save Brush Stoke**: *Only available when **Data Gather Mode** is set to 'Manual'.* Saves all brush strokes after the last **Save Brush Stroke**, **Flood Canvas**, or change in the **Data Gather Mode** to a dataset. 
- **Reset Stroke**: *Only available when **Data Gather Mode** is set to 'Manual'.* Clears current brush stroke data so a new brush stroke can be create. 
- **Flood Canvas**: Fills the entire canvas with a single Greyscale Hue defined by the users brush selection. (Clears current brush stroke data when **Data Gather Mode** is set to 'Manual')
- **Load Image**: Allows the user to select a png from their file system and loads the Image onto the canvas as a 128x128 greyscale image. (Clears current brush stroke data when **Data Gather Mode** is set to 'Manual')
- **Configure Data**: Opens the Congifure Data window where users can select Databases to save to and to generate from. 
##### Configure Data Window
- **Create New Database**: Allows the user to name and create a new Database. Relevent Folders are made in file system. 
- **Delete Existing Database**: Allows the user to select and delete a database.
- **Compile Data**: Prepares data for generation. Users can select to Mirror data Horizontally, Vertically, and to Rotate the data three times. 

## Purposed Features

- **Reset Button**: Resets current dataset. Currently requires program to be restarted. 
- **Metadata**: Store information of settings for future loading. 
- **Undo Button**: ability to revert to previous values. 
- **Limit duplicate windows**: Config Data Window and others will not produce duplicates 
- **Adv Generation Multiple Database Options**: Choose which database you wish to generate from. 
- **Update database or dataset**: Allow users to look through databases or datasets. 


