
# Converting the FBX models to NIfTI format

The first step in converting the model from FBX to Nifti is extracting the mesh from the volume model. This mesh is stored as an STL file. STL format stores only the structure (geometry) of the 3D model overlooking all other attributes. This can be done using MeshLab software. MeshLab is a tool for loading, editing, converting, and extracting mesh from 3D models stored as FBX or OBJ files [1].

For further steps, follow the steps in 'stl_to_nii.ipynb'.

Link to the models in FBX format: https://drive.google.com/drive/folders/1pJt8K0t-EwaTqaNDfNScAj0SKXUwCADs?usp=sharing

Link to download MeshLab: https://www.meshlab.net/#download

# Generating a Similarity matrix

To calculate the degree of similarity between any two kidney models, we calculated the similarity scores between their antsimages. After getting the models into NIfTI format, they can be loaded into ANTs for computing the similarity between them.

Follow steps in 'generating_similarity_matrix.ipynb' for generating the similarity matrix.

# Aligning the Kidney models

For creating a consensus kidney model, the mappings are computed between pairs of male and female kidneys.

See the file 'consensus_kidney_model.ipynb' for the steps.

# Libraries and modules required
1. ants (visit https://github.com/ANTsX/ANTsPy for installation guide)

2. trimesh

3. numpy-stl

4. vtkplotter

# References
[1] Cignoni, P., et al., MeshLab: an Open-Source Mesh Processing Tool. Sixth Eurographics Italian Chapter Conference, 2008: p. 129 - 136.
[2] Trimesh [Computer software]. 2019  07/10/2020]; Available from: https://github.com/mikedh/trimesh.
