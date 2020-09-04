
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/cns-iu/ccf-research-ftu">
    <img src="images/cns-logo-1.png" alt="Logo">
  </a>

  <h3 align="center">Common Coordinate Framework (CCF) Research on Functional Tissue Units (FTU)</h3>

  <p align="center">
    FTU Segmentation through Machine Learning (ML) Algorithms
    <br />
    <a href="https://github.com/cns-iu/ccf-research-ftu"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Data](#data)
  * [Algorithms](#algorithms)
* [Documentation](#documentation)
* [ML Pipelines](#ml-pipelines)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

The Human BioMolecular Atlas Program (HuBMAP) aims to create an open, global atlas of the human body at the cellular level. One component of this overarching goal is to identify glomeruli, functional tissue units (FTUs) consisting of capillaries that facilitate filtration of blood, within whole slide images of kidney tissue. Once these glomeruli are detected in the microscopy images, information on size and location within the kidney samples can be used to build a spatially accurate model of human kidneys for the HuBMAP.

Manual identification and classification of FTUs from microscopy images requires highly trained experts and is labor intensive. Many ML algorithms have been previously applied to automate detection of glomeruli. For this work, the Faster R-CNN and Mask R-CNN ML algorithms were utilized to detect glomeruli in Periodic acid-Schiff (PAS) stained whole slide images of kidney tissue samples. Faster R-CNN and Mask R-CNN are both convolutional neural network (CNN) algorithms designed for object detection in images. The Faster R-CNN algorithm outputs bounding  boxes around identified glomeruli, which are described by x-min, x-max, y-min, and y-max measures within the context of the original slide image. The Mask R-CNN algorithm takes this a step further, outputting a pixel-wise map of glomeruli vs. non-glomeruli sections of arbitrary shape from the input image.
A
Future work will include application of more ML algorithms, such as AlexNet, to FTUs from other tissues, such as colonic crypts.

### Data

Current work has focused on segmentation of glomeruli in PAS stained kidney whole slide images. Manual annotations of glomeruli within these images were produced as training material for the algorithms. The output segmentation results vary in form and include bounding boxes and binary, pixel-wise masks.

Future work will also incoorporate alternative imaging methods and tissue types.

#### Kidney

* [TMC-Vanderbilt Raw Data](https://drive.google.com/drive/folders/14aLxPR9LlzdWXPomAX1moqL0UnRm_RbW?usp=sharing)

#### Colon

This data has yet to be segmented by our ML algorithms, but it is the focus of future developments.

* [TMC-Stanford Raw Data - Accessible to IU Users Only](https://drive.google.com/drive/folders/1CL59rcrqlYFnug9B0XMn1KVMDQJFgy9D?usp=sharing)
* [TMC-Stanford Manual Annotation Data - Accessible to IU Users Only](https://drive.google.com/drive/folders/14HFeXnBfysOfnPdoynVwjxNEvChL1Jvz?usp=sharing)
* [TMC-Stanford Manual Annotation Images - Accessible to IU Users Only](https://drive.google.com/drive/folders/1jXjAYel2TTmQ1vo9JWGuO0SlNkuxjKnb?usp=sharing)

### Algorithms

#### Faster R-CNN
The Faster RCNN algorithm is one type of CNN used for object detection in images. CNNs employ neural networks for   deep learning and allow unsupervised feature generation. This algorithm takes an image as input, which it then divides into smaller rectangular regions. From then on, it considers each region to be a separate image. Next, these regions are passed to the CNN, which provides classes and bounding boxes for detected objects. In the case of kidney segmentation, the classes are ”Glomeruli” or ”Non-Glomeruli”. After this is complete for all regions, they are combined to make the original image with glomeruli detected in rectangular boxes. The algorithm outputs the data describing these detection boxes as separate rows in a CSV file which describes each annotation prediction as a single row of data. Fields include ”filename”, ”xmin”, ”xmax”, ”ymin”, and ”ymax”. The ”filename” refers to the unique number given to the region of the original image where the annotation was detected.

![Faster R-CNN Diagram](https://github.com/cns-iu/ccf-research-ftu/blob/master/images/FasterRCNNblockdiagram.png)

#### Mask R-CNN
The Mask RCNN algorithm is built upon the Faster RCNN algorithm, but it employs an instance segmentation extension that allows prediction of segmentation masks for each annotation. Rather than relying on the rectangular regions of the Faster RCNN algorithm for outputting detection boxes, the Mask RCNN provides a classification of ”Glomeruli” or ”Non-Glomeruli” to each pixel in the original image. This allows the resulting annotations to be any shape describable by pixels and enables the creation of binary mask overlays for use on the original image.
![Mask R-CNN Diagram](https://github.com/cns-iu/ccf-research-ftu/blob/master/images/MaskRCNNdiagram.jpg)

#### AlexNet
(Insert AlexNet overview.)

![AlexNet Diagram]()


<!-- GETTING STARTED -->
## Documentation

Refer to each algorithm's documentation for how it was implemented.

* [Faster R-CNN Documentation](https://github.com/cns-iu/ccf-research-ftu/blob/master/documentation/FasterRCNNDocumentation.md)
* [Mask R-CNN Documentation](https://github.com/cns-iu/ccf-research-ftu/blob/master/documentation/MaskRCNNDocumentation.md)
* [AlexNet Documentation]()


<!-- ML Pipelines-->
## ML Pipelines

![Faster R-CNN Pipeline](https://github.com/cns-iu/ccf-research-ftu/blob/master/images/pipeline%20images/Faster%20RCNN%20Pipeline.jpg)

![Mask R-CNN Pipeline](https://github.com/cns-iu/ccf-research-ftu/blob/master/images/pipeline%20images/Mask%20RCNN%20Pipeline.jpg)

(Insert AlexNet Pipeline image here.)


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Yingnan Ju - yiju@iu.edu

Leah Scherschel - [@LeahScherschel](https://twitter.com/LeahScherschel) - llschers@iu.edu

Project Link: [https://github.com/cns-iu/ccf-research-ftu](https://github.com/cns-iu/ccf-research-ftu)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [HuBMAP](https://www.hubmapconsortium.org/)
* [BIOmolecular Multimodal Imaging Center (BIOMIC) at Vanderbilt University](https://medschool.vanderbilt.edu/biomic/)
* [Snyder Lab at Stanford University's Department of Genetics](http://med.stanford.edu/snyderlab.html)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

