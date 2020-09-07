# StegoVis
We propose StegoVis to integrate visualization images with original data and exploration records. StegoVis can restore the exploration records on the image and allow users to interact with the original data. To resist users' graphical annotations on the images, StegoVis encodes the data into the QR codes with optimizing the parameters through integer programming and then arranges the pixels of QR codes into the LSBs of visualization images. We implement a prototype system to generate StegoVis or extract data from StegoVis. Our experiment validates that StegoVis does not influence the perception of original visualization, and can facilitate users' understanding and explorations in the real-world application scenarios.

![Integrating Visualization with Original Data](https://github.com/GeorgeProjects/StegoVis/blob/master/figures/stegovis-teaser.png)

This repository is a prototype system of StegoVis.

![Integrating Visualization with Original Data](https://github.com/GeorgeProjects/StegoVis/blob/master/figures/stego-vis-interface.png)

The following is the interface of StegoVis prototype system.
Users can upload the figure with embedding original data into *Painting panel*, and extract the underlying data into *Data panel*, and exploration records into *Timeline panel*. Users can brush the range in the painting panel to select the interested underlying data.

The following is a short demo video of the StegoVis prototype syste,.
![The demo of Stego vis prototype system](https://github.com/GeorgeProjects/StegoVis/blob/master/figures/stegovis-demo-video.mp4)


# How to run StegoVis prototype system?

## Start Backend:
1. `cd server`  *enter the back end of prototype system*
2. `python main.py`  *run the server*.
If the terminal shows "isten 14453....", it means that the server starts running.

## Start FrontEnd
1. `cd client`  *enter the front end of prototype system*
2. `npm run serve`  *run the client*. 
If the terminal shows: "App running at: Local: xxxxx Network: xxxxxx", it means that the client starts running.

3. Open browser and visit http://http://localhost:8080, and then can use Tree Illustraotr.